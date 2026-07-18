from django.contrib.auth import authenticate, get_user_model
from django.core import signing
from rest_framework import serializers

User = get_user_model()
RESET_TOKEN_SALT = 'accounts.password-reset'
RESET_TOKEN_MAX_AGE = 60 * 10  # 10 minutes, must match OTP expiry expectations


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Invalid email or password.')
        if not user.is_active:
            raise serializers.ValidationError('This account is inactive.')
        attrs['user'] = user
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email__iexact=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')
        self.context['user'] = user
        return value


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        from .models import PasswordResetOTP

        try:
            user = User.objects.get(email__iexact=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid or expired code.')

        otp = (
            PasswordResetOTP.objects.filter(user=user, code=attrs['otp'], is_used=False)
            .order_by('-created_at')
            .first()
        )
        if otp is None or otp.is_expired():
            raise serializers.ValidationError('Invalid or expired code.')

        attrs['user'] = user
        attrs['otp_instance'] = otp
        return attrs

    def make_reset_token(self, user):
        return signing.dumps({'user_id': user.pk}, salt=RESET_TOKEN_SALT)


class ResetPasswordSerializer(serializers.Serializer):
    reset_token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_reset_token(self, value):
        try:
            data = signing.loads(value, salt=RESET_TOKEN_SALT, max_age=RESET_TOKEN_MAX_AGE)
        except signing.BadSignature:
            raise serializers.ValidationError('Reset link expired or invalid. Start over.')
        try:
            user = User.objects.get(pk=data['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Reset link expired or invalid. Start over.')
        self.context['user'] = user
        return value
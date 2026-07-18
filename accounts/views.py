from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PasswordResetOTP, Token
from .serializers import (
    ForgotPasswordSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    VerifyOtpSerializer,
)

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(
            user=user,
            platform=request.data.get("platform", "android")
        )
        

        return Response({
            "token": token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'phone': user.phone,
                'address': user.address,
            },
        })


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email__iexact=email).first()

        # Always return success even if the email isn't found — don't leak
        # which emails are registered.
        if user is not None:
            otp = PasswordResetOTP.generate_for(user)
            print(otp.code)
            send_mail(
                subject='Your Solarblocks verification code',
                message=f'Your verification code is {otp.code}. It expires in 10 minutes.',
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )
            # DEV NOTE: with EMAIL_BACKEND set to console, the OTP prints to
            # your runserver terminal instead of a real inbox.

        return Response({'message': 'If that email exists, a code has been sent.'})


class VerifyOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        otp = serializer.validated_data['otp_instance']
        otp.is_used = True
        otp.save(update_fields=['is_used'])

        reset_token = serializer.make_reset_token(user)
        return Response({'reset_token': reset_token})


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.context['user']
        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        return Response({'message': 'Password updated. You can log in with your new password.'})
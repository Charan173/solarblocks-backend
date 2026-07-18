from django.urls import path
 
from .views import ForgotPasswordView, LoginView, ResetPasswordView, VerifyOtpView
 
urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='auth-forgot-password'),
    path('verify-otp/', VerifyOtpView.as_view(), name='auth-verify-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='auth-reset-password'),
]
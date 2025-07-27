from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, ResetPasswordView, ProfileUpdateView

app_name = "accounts"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # ثبت‌نام
    path('login/', LoginView.as_view(), name='login'),           # ورود
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # رفرش توکن
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'), # ریست رمز عبور
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'), # به‌روزرسانی پروفایل کاربری
]

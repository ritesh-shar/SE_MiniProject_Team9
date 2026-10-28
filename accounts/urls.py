"""
URL patterns for the accounts app (registration, login, token refresh).

# BBMS-F-001: /api/auth/register
# BBMS-F-002: /api/auth/login
# BBMS-SR-005: /api/auth/token/refresh
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('register/', RegisterView.as_view(), name='register-slash'),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('login/', TokenObtainPairView.as_view(), name='login-slash'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh-slash'),
]

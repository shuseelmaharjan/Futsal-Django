from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register-user', RegisterUserAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('user-token', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-role', GetUserRoleAPIView.as_view(), name='get_user_role'),
]

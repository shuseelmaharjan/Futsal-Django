from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register-user', RegisterUserAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-role', UserRoleAPIView.as_view(), name='get_user_role'),
    path('username', GetUsernameAPIView.as_view(), name='get_username'),
    path('user-id', GetUserIdAPIView.as_view(), name='get_user-id'),
    path('validate-token', ValidateTokenAPIView.as_view()),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('user-info', UserDataAPIView.as_view(), name='user-info'),
]

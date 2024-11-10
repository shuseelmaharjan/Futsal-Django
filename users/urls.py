from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register-user', RegisterUserAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-role', UserRoleAPIView.as_view(), name='get_user_role'),
    path('logout', LogoutAPIView.as_view(), name='logout'),

]

from django.urls import path
from .views import *

urlpatterns = [
    path('register-futsal', FutsalCreateAPIView.as_view(), name='register-futsal'),
    path('register-futsal/<int:pk>', FutsalDeleteAPIView.as_view(), name='register-futsal')
]

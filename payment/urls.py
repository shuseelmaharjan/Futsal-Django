from django.urls import path
from .views import *

urlpatterns = [
    path('create-payment', PaymentCreateAPIView.as_view(), name='create-payment'),
    path('user-payments', UserPaymentsView.as_view(), name='user-payments'),
]

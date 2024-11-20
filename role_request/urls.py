from django.urls import path
from .views import *

urlpatterns = [
    path('user-documents', UserDocumentsCreateAPIView.as_view(), name='user-documents-create'),
    path('update-vendor-status/<int:id>/<int:user_id>', UpdateStatusAPIView.as_view(), name='update-vendor-status'),
    path('pending-verification', PendingUpdateAPIView.as_view(), name='pending-verification'),
]
from django.urls import path
from .views import *

urlpatterns = [
    path('add-futsal', FutsalCreateView.as_view(), name='futsal-create'),
    path('list-futsals', UserFutsalListView.as_view(), name='user-futsal-list'),
    path('check-user-existence', CheckUserExistence.as_view(), name='check_user_existence'),
    path('update-futsal/<int:futsal_id>', UpdateFutsalAPIView.as_view(), name='update-futsal'),
]

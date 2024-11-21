from django.urls import path
from .views import *

urlpatterns = [
    path('create-booking', BookingCreateAPIView.as_view(), name='booking-create'),
    path('reservation-check', ReservationCheckAPIView.as_view(), name='reservation-check'),
    path('confirm-booking', ConfirmBookingAPIView.as_view(), name="confirm-booking"),
    path('update-booking-status', UpdateStatusAPIView.as_view(), name="update-booking-status"),
    path('cancel-booking', CancelBookingAPIView.as_view(), name="cancel-booking"),
    path('rebook-reservation', ReBookBookingAPIView.as_view(), name="rebook-booking"),
    path('bookings', UserBookingsAPIView.as_view(), name='user_bookings'),
    path('futsal-bookings', FutsalBookingsAPIView.as_view(), name="futsal-bookings"),
    path('booking-stats', BookingStatsView.as_view(), name='booking-stats'),
    path('futsal-owner-stat', FutsalBookingStatsAPIView.as_view(), name='futsal-owner-stat')
]

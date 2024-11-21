from django.db import models
from futsal.models import Futsal
from users.models import CustomUser
from datetime import datetime, time

class Booking(models.Model):
    futsal = models.ForeignKey(Futsal, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings")
    start_time = models.TimeField()
    end_time = models.TimeField()
    booking_date = models.DateField()
    is_confirmed = models.BooleanField(default=False, blank=True, null=True)
    is_reserved = models.BooleanField(default=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True, blank=True, null=True)

    def update_status(self):
        now = datetime.now()
        if self.booking_date == now.date() and self.end_time <= now.time():
            self.status = False
            self.save()

    def __str__(self):
        return str(self.id)

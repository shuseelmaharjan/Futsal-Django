from rest_framework import serializers

from futsal.models import Futsal
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class FutsalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Futsal
        fields = '__all__'


class UserBookingSerializer(serializers.ModelSerializer):
    futsal = FutsalSerializer()

    class Meta:
        model = Booking
        fields = '__all__'
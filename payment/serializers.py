from rest_framework import serializers

from futsal.serializers import FutsalListSerializer
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['booking', 'user', 'payment_amount', 'screenshot', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        return data

class ListPaymentSerializer(serializers.ModelSerializer):
    futsal = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['booking', 'user', 'payment_amount', 'screenshot', 'created_at', 'futsal']
        read_only_fields = ['created_at']

    def get_futsal(self, obj):
        if obj.booking and hasattr(obj.booking, 'futsal'):
            return FutsalListSerializer(obj.booking.futsal).data
        return None

    def validate(self, data):
        return data
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from reservation.models import Booking
from payment.models import Payment
from futsal.models import Futsal
from users.models import CustomUser


class PaymentCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Deserialize the incoming data
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            payment = serializer.save()
            return Response(
                {
                    "message": "Payment created successfully",
                    "payment_id": payment.id,
                    "payment_amount": str(payment.payment_amount),
                    "user": payment.user.username,
                    "booking_id": payment.booking.id,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

class UserPaymentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        payments = Payment.objects.filter(user=user)

        if not payments.exists():
            return Response({"detail": "No payments found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ListPaymentSerializer(payments, many=True)

        return Response(serializer.data)


class UserFutsalPaymentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            futsal = Futsal.objects.get(user_id=user)
        except Futsal.DoesNotExist:
            return Response(
                {"message": "No futsal found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        payments = Payment.objects.filter(booking__futsal=futsal)

        if not payments.exists():
            return Response(
                {"message": "No payments found for this futsal."},
                status=status.HTTP_404_NOT_FOUND
            )

        payment_data = [
            {
                "payment_id": payment.id,
                "booking_id": payment.booking.id,
                "payment_amount": str(payment.payment_amount),
                "payment_date": payment.created_at.isoformat(),
                "screenshot": payment.screenshot.url if payment.screenshot else None,
                "user_details": {
                    "name": payment.booking.user.name,
                    "email": payment.booking.user.email,
                    "phone": payment.booking.user.phone
                }
            }
            for payment in payments
        ]
        return Response(
            {
                "payments": payment_data
            },
            status=status.HTTP_200_OK
        )

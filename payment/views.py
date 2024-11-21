from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializers import *
from rest_framework.permissions import IsAuthenticated

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
from http.client import responses

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from payment.models import Payment
from .models import Booking
from .serializers import *
from django.utils.timezone import now
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated


class BookingCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        futsal_id = data.get("futsal")
        booking_date = data.get("booking_date")
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        existing_booking = Booking.objects.filter(
            futsal_id=futsal_id,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time
        ).exclude(status=False).exists()

        if existing_booking:
            return Response(
                {"message": "A booking with the same details already exists and is confirmed. Now proceed to payment."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            booking = serializer.save()
            booking_id = booking.id
            return Response(
                {
                    "message": "Booking created successfully",
                    "booking_id": booking_id
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class ReservationCheckAPIView(APIView):
    def post(self, request, *args, **kwargs):
        futsal_id = request.data.get('futsal_id')
        start_time_str = request.data.get('start_time')
        end_time_str = request.data.get('end_time')
        booking_date = request.data.get('booking_date')

        if not all([futsal_id, start_time_str, end_time_str, booking_date]):
            return Response({"error": "All fields (futsal_id, start_time, end_time, booking_date) are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Enforce the use of 24-hour format
            start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
            end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()

            # Filter bookings for the given futsal and date
            existing_bookings = Booking.objects.filter(
                futsal_id=futsal_id,
                booking_date=booking_date
            )

            for booking in existing_bookings:
                # Check for overlap in time slots
                if (
                    (start_time >= booking.start_time and start_time < booking.end_time) or
                    (end_time > booking.start_time and end_time <= booking.end_time) or
                    (start_time <= booking.start_time and end_time >= booking.end_time)
                ):
                    # Booking exists in the requested time slot
                    if booking.is_confirmed and booking.is_reserved:
                        return Response({
                            "status": "unavailable",
                            "message": f"Futsal already booked from {booking.start_time} to {booking.end_time}. Next available time after {booking.end_time}."
                        })
                    else:
                        time_difference = now() - booking.created_at
                        if time_difference <= timedelta(minutes=5) and not booking.is_confirmed:
                            return Response({
                                "status": "available",
                                "message": "Reservation is temporarily held but not confirmed. You can book now."
                            })

            # If no overlapping booking exists
            return Response({"status": "available", "message": "Reservation is available."})

        except ValueError:
            return Response({"error": "Invalid time format. Use HH:MM:SS format for start_time and end_time."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConfirmBookingAPIView(APIView):
    def post(self, request):
        booking_id = request.data.get("booking_id")
        user_id = request.data.get("user_id")
        futsal_id = request.data.get("futsal_id")
        print(request.data)
        if not all([booking_id, user_id, futsal_id]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the booking instance
            booking = Booking.objects.get(id=booking_id, user_id=user_id, futsal_id=futsal_id)

            # Update the is_confirmed field
            booking.is_confirmed = True
            booking.save()

            return Response({"message": "Booking confirmed successfully."}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateStatusAPIView(APIView):
    def post(self, request):
        booking_id = request.data.get("booking_id")
        user_id = request.data.get("user_id")
        futsal_id = request.data.get("futsal_id")

        if not all([booking_id, user_id, futsal_id]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the booking instance
            booking = Booking.objects.get(id=booking_id, user_id=user_id, futsal_id=futsal_id)

            # Update the is_confirmed field
            booking.status = False
            booking.save()

            return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CancelBookingAPIView(APIView):
    def post(self, request):
        reservation_id = request.data.get("booking_id")
        user_id = request.data.get("user_id")
        futsal_id = request.data.get("futsal_id")

        # Validate that all required fields are present
        if not all([reservation_id, user_id, futsal_id]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the booking instance
            booking = Booking.objects.get(id=reservation_id, user_id=user_id, futsal_id=futsal_id)

            # Update the fields
            booking.is_confirmed = False
            booking.is_reserved = False
            booking.status = False
            booking.save()

            return Response({"message": "Booking canceled successfully."}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReBookBookingAPIView(APIView):
    def post(self, request):
        id = request.data.get("booking_id")
        user_id = request.data.get("user_id")
        futsal_id = request.data.get("futsal_id")

        # Validate that all required fields are present
        if not all([id, user_id, futsal_id]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the booking instance
            booking = Booking.objects.get(id=id, user_id=user_id, futsal_id=futsal_id)

            # Update the fields
            booking.is_confirmed = True
            booking.is_reserved = True
            booking.status = True
            booking.save()

            return Response({"message": "Booking updated successfully."}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        bookings = Booking.objects.filter(user_id=user)

        if not bookings.exists():
            return Response({"message": "No bookings found for this user."}, status=status.HTTP_404_NOT_FOUND)

        booking_data = []
        for booking in bookings:
            # Check if the user has made a payment for the booking
            payment = Payment.objects.filter(booking=booking, user=user).first()

            # Determine if the payment status is "Paid" or "Unpaid"
            payment_status = 'Paid' if payment else 'Unpaid'

            # Serialize the booking data
            booking_info = UserBookingSerializer(booking).data
            booking_info['payment_status'] = payment_status  # Add payment status to the response

            booking_data.append(booking_info)

        return Response(booking_data, status=status.HTTP_200_OK)


class BookingStatsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        last_3_bookings = Booking.objects.all().order_by('-created_at')[:3]
        serializer = UserBookingSerializer(last_3_bookings, many=True)

        total_bookings = Booking.objects.count()

        total_confirmed_reserved = Booking.objects.filter(is_confirmed=True, is_reserved=True).count()

        total_confirmed_reserved_status_false = Booking.objects.filter(is_confirmed=True, is_reserved=True, status=False).count()

        response_data = {
            "last_3_bookings": serializer.data,
            "total_bookings": total_bookings,
            "total_confirmed_reserved": total_confirmed_reserved,
            "total_confirmed_reserved_status_false": total_confirmed_reserved_status_false,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class FutsalBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Fetch the futsal associated with the logged-in user
        try:
            futsal = Futsal.objects.get(user_id=user)
        except Futsal.DoesNotExist:
            return Response({"message": "No futsal found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all bookings for the futsal
        bookings = Booking.objects.filter(futsal=futsal)

        if not bookings.exists():
            return Response({"message": "No bookings found for this futsal."}, status=status.HTTP_404_NOT_FOUND)

        booking_data = []
        for booking in bookings:
            # Check if a payment exists for the user associated with the booking
            try:
                payment = Payment.objects.get(booking=booking, user=booking.user)  # Check for the user of the booking
                payment_status = 'Paid'
            except Payment.DoesNotExist:
                payment_status = 'Unpaid'

            # Serialize the booking data
            booking_info = BookingSerializer(booking).data
            booking_info['payment_status'] = payment_status

            # Include user information in the response
            user_info = {
                'id': booking.user.id,
                'phone': booking.user.phone,
                'name': booking.user.name,
            }
            booking_info['user'] = user_info

            booking_data.append(booking_info)

        return Response(booking_data, status=status.HTTP_200_OK)


class FutsalBookingStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the authenticated user
        user = request.user

        # Retrieve the Futsal associated with the user
        futsal = Futsal.objects.filter(user_id=user).first()

        if not futsal:
            return Response({"message": "No futsal found for the authenticated user."},
                            status=status.HTTP_404_NOT_FOUND)

        # Get the current date (today)
        today = timezone.now().date()

        # Total bookings for the given futsal
        total_bookings = Booking.objects.filter(futsal=futsal).count()

        # Bookings with specific statuses
        total_confirmed = Booking.objects.filter(futsal=futsal, is_confirmed=True).count()
        total_reserved = Booking.objects.filter(futsal=futsal, is_reserved=True).count()
        total_status_false = Booking.objects.filter(futsal=futsal, status=False).count()

        # Bookings created today
        bookings_today = Booking.objects.filter(futsal=futsal, created_at__date=today).count()

        # Prepare the response data
        stats = {
            "total_bookings": total_bookings,
            "total_confirmed": total_confirmed,
            "total_reserved": total_reserved,
            "total_status_false": total_status_false,
            "bookings_today": bookings_today
        }

        return Response(stats, status=status.HTTP_200_OK)

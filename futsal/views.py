from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import CustomUser
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from math import radians, sin, cos, sqrt, atan2

class FutsalCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FutsalSerializer(data=request.data)

        if serializer.is_valid():
            futsal = serializer.save(user_id=request.user)
            return Response({"message": "Futsal created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFutsalListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        futsals = Futsal.objects.filter(user_id=user)
        serializer = FutsalSerializer(futsals, many=True)
        return Response(serializer.data)



class CheckUserExistence(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        futsal_exists = Futsal.objects.filter(user_id=user).exists()

        if futsal_exists:
            return Response({'message': 'User exists in futsal table', 'exists': True}, status=200)
        else:
            return Response({'message': 'User does not exist in futsal table', 'exists': False}, status=404)

class UpdateFutsalAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, futsal_id):
        try:
            futsal = Futsal.objects.get(id=futsal_id, user_id=request.user)
        except Futsal.DoesNotExist:
            return Response({"detail": "Futsal not found or you do not have permission to edit this futsal."},
                             status=status.HTTP_404_NOT_FOUND)

        serializer = FutsalSerializer(futsal, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FutsalListView(APIView):
    def get(self, request):
        try:
            futsals = Futsal.objects.all()  # Fetch all futsal records
            serializer = FutsalListSerializer(futsals, many=True)  # Serialize the queryset
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class FutsalDetailView(APIView):
    def get(self, request, slug):
        try:
            futsal = Futsal.objects.get(slug=slug)
        except Futsal.DoesNotExist:
            return Response({'error': 'Futsal not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FutsalSerializer(futsal)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CheckSlugExistence(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SlugCheckSerializer(data=request.data)
        if serializer.is_valid():
            slug = serializer.validated_data['slug']
            # Check if the slug exists in the database
            if Futsal.objects.filter(slug=slug).exists():
                return Response({"exists": True}, status=status.HTTP_200_OK)
            else:
                return Response({"exists": False}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardStats(APIView):
    def get(self, request):
        try:
            # Get counts of different user types
            total_admins = CustomUser.objects.filter(is_admin=True).count()
            total_users = CustomUser.objects.filter(is_guest=True).count()
            total_vendors = CustomUser.objects.filter(is_vendor=True).count()

            # Get the count of Futsals
            total_futsals = Futsal.objects.count()

            # Response data
            data = {
                "total_admins": total_admins,
                "total_users": total_users,
                "total_vendors": total_vendors,
                "total_futsals": total_futsals
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Difference of latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = R * c  # Distance in kilometers
    return distance

class NearestFutsalsView(APIView):
    def post(self, request):
        # Parse JSON body
        data = request.data

        # Check if the required fields are present in the body
        lat = data.get('latitude')
        lon = data.get('longitude')
        radius = data.get('radius', 10)  # Default radius is 10 km if not provided

        if lat is None or lon is None:
            return Response({"error": "Latitude and Longitude are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convert lat, lon, and radius to the correct types
            lat = float(lat)
            lon = float(lon)
            radius = float(radius)

            # Fetch all futsals
            futsals = Futsal.objects.all()

            # Filter futsals by distance
            nearest_futsals = []
            for futsal in futsals:
                futsal_lat = futsal.latitude
                futsal_lon = futsal.longitude
                distance = haversine(lat, lon, futsal_lat, futsal_lon)

                # If the distance is within the specified radius, include it
                if distance <= radius:
                    nearest_futsals.append((futsal, distance))

            # Sort the futsals by distance
            nearest_futsals.sort(key=lambda x: x[1])

            # Format the response
            response_data = []
            for futsal, distance in nearest_futsals[:5]:
                response_data.append({
                    'id': futsal.id,
                    'name': futsal.name,
                    'location': futsal.location,
                    'slug':futsal.slug,
                    'phone':futsal.phone,
                    'distance': round(distance, 2),
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid latitude, longitude, or radius."}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated

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
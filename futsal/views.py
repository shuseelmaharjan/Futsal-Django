from django.shortcuts import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import *
from futsal.serializers import *
from futsal.models import *

# Create your views here.
class FutsalCreateAPIView(APIView):
    def post(self, request):
        serializer = FutsalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Futsal created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FutsalDeleteAPIView(APIView):
    def delete(self, request, pk, format=None):
        try:
            faculty = Futsal.objects.get(pk=pk)
            faculty.delete()
            return Response({"message":"Futsal deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Futsal.DoesNotExist:
            return Response({"message":"Row doesnot exist"},status=status.HTTP_404_NOT_FOUND)
    
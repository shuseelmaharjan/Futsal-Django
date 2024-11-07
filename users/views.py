from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
class GetUserRoleAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user  # Get the current authenticated user

        # Determine the role based on flags
        if user.is_admin:
            role = "admin"
        elif user.is_vendor:
            role = "vendor"
        elif user.is_guest:
            role = "user"
        else:
            role = "guest"  # You can handle the case if none of the flags are set

        # Generate the JWT token for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return the role and access token in the response
        return Response({
            "role": role,
            "access_token": access_token
        })
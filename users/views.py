from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, TokenError

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
            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ValidateTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.headers.get('Authorization', None)
        
        if token is None or not token.startswith('Bearer '):
            return Response({'error': 'Token not provided or invalid format'}, status=status.HTTP_400_BAD_REQUEST)
        
        access_token = token.split()[1]

        try:
            AccessToken(access_token)
            return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'error': 'Token is expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
     
class UserRoleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserRoleSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetUsernameAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
        }, status=status.HTTP_200_OK)
    

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Print headers and body to help debug
        print("Request Headers:", request.headers)
        print("Request Data:", request.data)

        # Extract refresh token from the Authorization header
        refresh_token = request.headers.get('Authorization')

        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the "Bearer " prefix if it's present in the Authorization header
        if refresh_token.startswith('Bearer '):
            refresh_token = refresh_token.split(' ')[1]
        else:
            return Response({"detail": "Invalid token format. Ensure you send a Bearer token."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'username', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['status'] = "true"
        validated_data['is_guest'] = True
        validated_data['is_admin'] = False
        validated_data['is_vendor'] = False

        email = validated_data['email']
        username = validated_data['username']
        password = validated_data['password']

        extra_fields = {key: value for key, value in validated_data.items() if key not in ['email', 'username', 'password']}

        user = CustomUser.objects.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields  
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Authenticate user
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalis email or password.")

        data['user'] = user
        return data
    
class UserRoleSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['role']

    def get_role(self, obj):
        if obj.is_admin:
            return 'admin'
        elif obj.is_guest:
            return 'user'
        elif obj.is_vendor:
            return 'vendor'
        return 'unknown'

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        if new_password != confirm_password:
            raise serializers.ValidationError("New passwords do not match.")
        validate_password(new_password)
        return attrs

class CustomUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'username', 'phone', 'created_at']

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_guest', 'is_vendor']

    def update(self, instance, validated_data):
        instance.is_guest = validated_data.get('is_guest', instance.is_guest)
        instance.is_vendor = validated_data.get('is_vendor', instance.is_vendor)
        instance.save()
        return instance
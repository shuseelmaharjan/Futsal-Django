from rest_framework import serializers

from users.models import CustomUser
from .models import UserDocuments

class UserDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocuments
        fields = ['user', 'coverletter', 'registration']
        read_only_fields = ['date']


class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocuments
        fields = ['status']

class UsersInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'phone']

class UserDataSerializer(serializers.ModelSerializer):
    user = UsersInfoSerializer()

    class Meta:
        model = UserDocuments
        fields = '__all__'
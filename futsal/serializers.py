from rest_framework import serializers
from .models import Futsal

class FutsalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Futsal
        fields = ['id', 'name', 'description', 'image', 'location', 'phone', 'longitude', 'latitude']

    def update(self, instance, validated_data):
        # Custom update logic (optional)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.location = validated_data.get('location', instance.location)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.save()
        return instance


class FutsalImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Futsal
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
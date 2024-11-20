from rest_framework import serializers
from .models import Futsal
from rest_framework.fields import ImageField

class FutsalSerializer(serializers.ModelSerializer):
    image = ImageField(required=False)  # Ensure the image field is optional

    class Meta:
        model = Futsal
        fields = ['id', 'name', 'description', 'image', 'location', 'phone', 'longitude', 'latitude']

    def update(self, instance, validated_data):
        # Update all other fields
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.location = validated_data.get('location', instance.location)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)

        # Handle the image field
        image = validated_data.get('image')
        if isinstance(image, str):
            # If the image field is a string (existing path), keep the current image
            pass
        elif image:
            # If a new image is uploaded, update it
            instance.image = image

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

class NearestFutsalSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField()  # Custom field for distance

    class Meta:
        model = Futsal
        fields = ['id', 'name', 'distance', 'location', 'phone', 'latitude', 'longitude']


class FutsalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Futsal
        fields = '__all__'

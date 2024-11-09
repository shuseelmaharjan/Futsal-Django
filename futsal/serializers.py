from rest_framework import serializers
from futsal.models import *

class FutsalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Futsal
        fields = ['id', 'name', 'description']


from rest_framework import serializers
from .models import Filmography

class FilmoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filmography
        fields = '__all__'
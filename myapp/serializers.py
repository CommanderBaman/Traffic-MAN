from rest_framework import serializers
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
class CurrentImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentImages
        fields = '__all__'        

class TrafficLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficLight
        fields = '__all__'                
from rest_framework import serializers
from .models import Order
from flower.models import Flower  

class OrderSerializer(serializers.ModelSerializer):
    flower = serializers.PrimaryKeyRelatedField(queryset=Flower.objects.all())  # Serializing the related Flower
    
    class Meta:
        model = Order
        fields = '__all__'

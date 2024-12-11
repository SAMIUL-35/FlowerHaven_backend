from rest_framework import serializers
from .models import Flower
from category.serializers import CategorySerializer

class FlowerSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Serialize category field using CategorySerializer

    class Meta:
        model = Flower
        fields = '__all__'

from rest_framework import serializers
from .models import Flower
from category.models import Category
from category.serializers import CategorySerializer

class FlowerSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Flower
        fields = '__all__'


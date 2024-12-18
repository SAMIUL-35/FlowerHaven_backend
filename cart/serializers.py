from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    flower_name = serializers.CharField(source='flower.name', read_only=True)
    flower_id = serializers.IntegerField(source='flower.id', read_only=True)
    flower_price = serializers.DecimalField(source='flower.price', read_only=True, max_digits=10, decimal_places=2)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'flower', 'flower_name', 'flower_id', 'flower_price', 'quantity', 'created_at', 'updated_at', 'total_price','purchased' ]

    def get_total_price(self, instance):
        """Calculate the total price for the cart item."""
        if not isinstance(instance, Cart):
            raise serializers.ValidationError("Instance must be of type Cart.")
        return round(instance.flower.price * instance.quantity, 2)

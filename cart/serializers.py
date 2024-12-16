from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    flower_name = serializers.CharField(source='flower.name', read_only=True)
    flower_id = serializers.IntegerField(source='flower.id', read_only=True)  # Include flower ID
    flower_price = serializers.DecimalField(source='flower.price', read_only=True, max_digits=10, decimal_places=2)
    total_price = serializers.SerializerMethodField()  # Custom field for total price

    class Meta:
        model = Cart
        fields = ['id', 'flower', 'flower_name', 'flower_id', 'flower_price', 'quantity', 'created_at', 'updated_at', 'total_price']

    def get_total_price(self, instance):
        """Calculate the total price for the cart item."""
        return instance.flower.price * instance.quantity  # Total price based on flower price and quantity

    def validate_quantity(self, value):
        """Ensure that the quantity is greater than zero."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

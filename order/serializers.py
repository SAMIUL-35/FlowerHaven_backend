from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order
from cart.serializers import CartSerializer

class OrderSerializer(serializers.ModelSerializer):
    cart_items = CartSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'username', 'cart_items', 'total_price', 'ordered', 'created_at', 'paymentId', 'orderId', 'status']

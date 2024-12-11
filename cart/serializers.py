from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # To display the username instead of the user ID
    flower = serializers.StringRelatedField(read_only=True)  # To display the flower name instead of the ID
    flower_id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), source='flower')  # For handling flower ID in requests

    class Meta:
        model = Cart
        fields = ['id', 'user', 'flower', 'flower_id', 'quantity', 'total_price']
        read_only_fields = ['total_price']

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.total_price()

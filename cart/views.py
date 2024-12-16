from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from .models import Cart, Flower
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
import logging

logger = logging.getLogger(__name__)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.select_related('flower').all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        flower = serializer.validated_data['flower']

        if flower.stock < 1:
            raise ValidationError({"detail": "This flower is out of stock."})

        existing_cart_item = Cart.objects.filter(user=self.request.user, flower=flower).first()

        try:
            if existing_cart_item:
                existing_cart_item.quantity += 1
                existing_cart_item.save()
            else:
                serializer.save(user=self.request.user)

            flower.stock = F('stock') - 1
            flower.save()

        except Exception as e:
            raise ValidationError({"detail": f"Failed to add item to cart: {str(e)}"})

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_quantity = int(request.data.get("quantity", instance.quantity))

        if new_quantity <= 0:
            flower = instance.flower
            flower.stock += instance.quantity
            flower.save()
            instance.delete()
            return Response({"detail": "Cart item removed."}, status=204)

        flower = instance.flower
        quantity_change = new_quantity - instance.quantity

        if quantity_change > 0 and flower.stock < quantity_change:
            raise ValidationError({"detail": "Not enough stock available."})

        flower.stock -= quantity_change
        flower.save()

        instance.quantity = new_quantity
        instance.save()

        total_price = instance.flower.price * instance.quantity

        return Response({
            "item": CartSerializer(instance).data,
            "total_price": total_price
        })

    @action(detail=False, methods=["get"], url_path="cart-total")
    def cart_total(self, request):
        logger.info("Cart total action called")

        cart_items = self.get_queryset()
        grand_total = sum(item.flower.price * item.quantity for item in cart_items)

        cart_item_data = CartSerializer(cart_items, many=True).data

        return Response({
            "cart_items": cart_item_data,
            "grand_total": grand_total
        })

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from .models import Cart, Flower
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated
import logging
from rest_framework.decorators import action

logger = logging.getLogger(__name__)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.select_related('flower').all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, purchased=False)

    @transaction.atomic
    def perform_create(self, serializer):
        flower = serializer.validated_data.get('flower')
        quantity = serializer.validated_data.get('quantity', 1)

        # Refresh stock and log its value
        flower.refresh_from_db()
        logger.debug(f"Stock for flower {flower.id}: {flower.stock}")
        logger.debug(f"Requested quantity: {quantity}")

        # Check stock availability
        if flower.stock < quantity:
            logger.error(f"Not enough stock available for flower {flower.id}")
            raise ValidationError({"detail": "Not enough stock available."})

        # Check for existing cart item (same product, purchased=False)
        existing_cart_item = Cart.objects.filter(user=self.request.user, flower=flower, purchased=False).first()

        if existing_cart_item:
            # Add quantity to the existing cart item
            new_quantity = existing_cart_item.quantity + quantity
            logger.debug(f"New quantity for existing cart item: {new_quantity}")

            # If the new quantity exceeds available stock, raise an error
            if quantity > flower.stock:
                logger.error(f"Not enough stock available for requested quantity. Available: {flower.stock}, Requested: {new_quantity}")
                raise ValidationError({"detail": "Not enough stock available for the requested quantity."})

            # Update the existing cart item with the new quantity
            existing_cart_item.quantity = new_quantity
            existing_cart_item.save()

        else:
            # No existing cart item, so create a new one
            serializer.save(user=self.request.user)

        # Deduct stock after adding to the cart
        flower.stock = F('stock') - quantity
        flower.save()
        flower.refresh_from_db()
        logger.debug(f"Updated stock for flower {flower.id}: {flower.stock}")

    @transaction.atomic
    def perform_destroy(self, instance):
        flower = instance.flower
        flower.stock += instance.quantity  # Increase stock when deleting the cart item
        flower.save()
        logger.debug(f"Stock restored for flower {flower.id}: {flower.stock}")
        super().perform_destroy(instance)

    @action(detail=False, methods=["get"], url_path="cart-total")
    def cart_total(self, request):
        logger.info(f"Cart total requested by user {request.user.id}")

        # Fetch cart items for the user that are not purchased
        cart_items = self.get_queryset()
        grand_total = sum(item.flower.price * item.quantity for item in cart_items)

        logger.debug(f"User {request.user.id} cart total: {grand_total}")

        # Serialize the cart items data
        cart_item_data = CartSerializer(cart_items, many=True).data

        # Return response with cart items and grand total
        return Response({
            "cart_items": cart_item_data,
            "grand_total": grand_total
        })

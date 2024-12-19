import logging
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from django.db import transaction
from django.conf import settings
from django.core.mail import send_mail
from .models import Order, Cart
from .serializers import OrderSerializer

logger = logging.getLogger(__name__)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user, purchased=False)

        if not cart_items.exists():
            raise ValidationError({"detail": "Your cart is empty."})

        if Order.objects.filter(user=request.user, ordered=False).exists():
            raise ValidationError({"detail": "You already have an active order."})

        total_price = sum(item.get_totals() for item in cart_items)

        order = Order.objects.create(user=request.user, total_price=total_price)

        order.cart_items.set(cart_items)
        order.save()

        Cart.objects.filter(user=request.user, purchased=False).update(purchased=True)

        Order.objects.filter(user=request.user, ordered=False).update(ordered=True)

        send_order_confirmation_email(request.user.email, order.id, total_price)

        return Response({
            "detail": "Order successfully created.",
            "order_id": order.id,
            "total_price": order.total_price,
        }, status=201)

    @action(detail=False, methods=["get"], url_path="order-history")
    def order_history(self, request):
        orders = self.get_queryset().filter(ordered=True)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

def send_order_confirmation_email(email, order_id, total_price):
    subject = "Order Confirmation - Your Order has been Placed!"
    message = (
        f"Thank you for your order!\n\n"
        f"Your order ID: {order_id}\n"
        f"Total Price: ${total_price}\n\n"
        f"We will notify you once your order is shipped."
    )
    email_from = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, email_from, [email], fail_silently=False)

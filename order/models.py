from django.db import models
from django.contrib.auth import get_user_model
from flower.models import Flower
from cart.models import Cart

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    cart_items = models.ManyToManyField(Cart, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=250, blank=True, null=True)
    orderId = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def update_stock_and_purchase(self):
        for cart_item in self.cart_items.all():
            flower = cart_item.flower
            flower.stock -= cart_item.quantity  # Deduct quantity from stock
            flower.save()
            cart_item.purchased = True  # Mark item as purchased
            cart_item.save()

    def calculate_total_price(self):
        total = sum(cart_item.get_totals() for cart_item in self.cart_items.all())
        return total

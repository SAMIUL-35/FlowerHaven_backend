from django.db import models
from django.contrib.auth import get_user_model
from flower.models import Flower

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.flower} ({self.quantity})"
    
    def get_totals(self):
        """Calculate the total price for this cart item."""
        return round(self.flower.price * self.quantity, 2)

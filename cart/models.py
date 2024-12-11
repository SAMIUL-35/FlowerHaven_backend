from django.db import models
from django.contrib.auth import get_user_model
from flower.models import Flower

User = get_user_model()  # Dynamically get the user model to ensure flexibility

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'flower'], name='unique_user_flower')
        ]

    def total_price(self):
        return self.quantity * self.flower.price

    def __str__(self):
        return f"{self.user.username}'s cart - {self.flower.name} x {self.quantity}"

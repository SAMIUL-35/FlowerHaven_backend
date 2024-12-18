from django.db import models
from django.contrib.auth import get_user_model
from flower.models import Flower
from cart.models import Cart

User = get_user_model()

class Order(models.Model):
    # Foreign key to the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    
    # Many to many relationship to Cart
    cart_items = models.ManyToManyField(Cart, related_name="orders")
    
    # Total price for the order
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Boolean to mark if the order is complete
    ordered = models.BooleanField(default=False)
    
    # Date and time when the order was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Payment ID associated with the order (can be null if not paid)
    paymentId = models.CharField(max_length=250, blank=True, null=True)
    
    # Order ID associated with the order (can be null if not completed)
    orderId = models.CharField(max_length=250, blank=True, null=True)
    
    # New field for order status (default is 'pending')
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending'
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def update_stock_and_purchase(self):
        """Update the stock and mark items as purchased when the order is completed."""
        for cart_item in self.cart_items.all():
            flower = cart_item.flower
            flower.stock -= cart_item.quantity  # Deduct quantity from stock
            flower.save()
            cart_item.purchased = True  # Mark item as purchased
            cart_item.save()

    def calculate_total_price(self):
        """Calculate the total price of the order based on the cart items."""
        total = sum(cart_item.get_totals() for cart_item in self.cart_items.all())
        return total

from django.db import models
from category.models  import Category

class Flower(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='flowers')
    image = models.ImageField(upload_to='flowers/images')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

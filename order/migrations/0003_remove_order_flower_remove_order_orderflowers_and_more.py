# Generated by Django 5.1.1 on 2024-12-15 10:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_cart_created_at_alter_cart_updated_at'),
        ('order', '0002_remove_order_quantity_remove_order_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='flower',
        ),
        migrations.RemoveField(
            model_name='order',
            name='orderFlowers',
        ),
        migrations.RemoveField(
            model_name='order',
            name='orderid',
        ),
        migrations.AddField(
            model_name='order',
            name='cart_items',
            field=models.ManyToManyField(related_name='orders', to='cart.cart'),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='orderId',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]

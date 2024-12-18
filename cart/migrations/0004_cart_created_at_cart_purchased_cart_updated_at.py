# Generated by Django 5.1.1 on 2024-12-14 18:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_cart_unique_user_flower'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='cart',
            name='purchased',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cart',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]

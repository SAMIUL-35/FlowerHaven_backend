# Generated by Django 5.1.1 on 2024-12-13 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_cart_user'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='cart',
            name='unique_user_flower',
        ),
    ]
# Generated by Django 5.1.1 on 2024-12-13 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flower',
            name='image',
            field=models.ImageField(upload_to='flower/images'),
        ),
    ]

# Generated by Django 5.1.4 on 2025-03-11 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0012_tbl_cart_color_tbl_cart_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_cart',
            name='image',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]

# Generated by Django 5.1.5 on 2025-03-03 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0005_tbl_contact_remove_tbl_register_username_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_cart',
            name='size',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

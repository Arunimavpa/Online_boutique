# Generated by Django 5.1.4 on 2025-02-20 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0002_tbl_product_tbl_productvariant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_product',
            name='vendor',
        ),
        migrations.RemoveField(
            model_name='tbl_productvariant',
            name='size',
        ),
        migrations.RemoveField(
            model_name='tbl_productvariant',
            name='stock',
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='Pattern',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='WashCare',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='fabric',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tbl_product',
            name='size',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

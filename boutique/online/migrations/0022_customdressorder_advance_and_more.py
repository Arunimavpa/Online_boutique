# Generated by Django 5.1.4 on 2025-03-17 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0021_order_d_date_order_p_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customdressorder',
            name='advance',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='customdressorder',
            name='payment_status',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customdressorder',
            name='total_cost',
            field=models.FloatField(null=True),
        ),
    ]

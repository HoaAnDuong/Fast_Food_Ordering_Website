# Generated by Django 4.1.6 on 2023-04-05 06:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0014_order_shipper_order_product_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.TextField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipper_orders', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.1.6 on 2023-04-21 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_product_pending_price_product_pending_price_currency_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='pending_price',
            new_name='new_price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='pending_price_currency',
            new_name='new_price_currency',
        ),
    ]

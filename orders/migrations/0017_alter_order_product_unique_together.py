# Generated by Django 4.1.6 on 2023-04-06 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_rename_name_product_status_code'),
        ('orders', '0016_remove_order_shipper'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='order_product',
            unique_together={('order', 'product')},
        ),
    ]
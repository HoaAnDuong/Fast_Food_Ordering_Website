# Generated by Django 4.1.6 on 2023-04-21 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_rename_product_status_order_product_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_product_status',
            old_name='name',
            new_name='code',
        ),
    ]

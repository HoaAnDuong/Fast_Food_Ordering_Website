# Generated by Django 4.1.6 on 2023-03-29 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_customer_alter_order_log_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='images',
        ),
    ]

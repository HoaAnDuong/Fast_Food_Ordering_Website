# Generated by Django 4.1.6 on 2023-03-01 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_store'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='store',
        ),
    ]
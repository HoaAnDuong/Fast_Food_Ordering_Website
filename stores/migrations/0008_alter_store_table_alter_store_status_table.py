# Generated by Django 4.1.6 on 2023-03-30 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0007_store_status_store_status'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='store',
            table='Store',
        ),
        migrations.AlterModelTable(
            name='store_status',
            table='Store_Status',
        ),
    ]
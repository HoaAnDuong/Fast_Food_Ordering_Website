# Generated by Django 4.1.6 on 2023-04-19 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_delivery_start_point_delivery_point_priority_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery_point',
            name='priority',
            field=models.PositiveIntegerField(default=1),
        ),
    ]

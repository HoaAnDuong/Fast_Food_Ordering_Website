# Generated by Django 4.1.6 on 2023-03-29 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_country_alter_location_address_alter_location_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]
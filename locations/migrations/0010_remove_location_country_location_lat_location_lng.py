# Generated by Django 4.1.6 on 2023-04-03 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0009_remove_location_postal_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='country',
        ),
        migrations.AddField(
            model_name='location',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='location',
            name='lng',
            field=models.FloatField(default=0),
        ),
    ]

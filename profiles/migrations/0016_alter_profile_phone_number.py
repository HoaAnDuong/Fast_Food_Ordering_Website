# Generated by Django 4.1.6 on 2023-04-04 08:07

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0015_alter_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region='VI', unique=True),
        ),
    ]

# Generated by Django 4.1.6 on 2023-04-06 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0020_profile_moderated'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='citizen_identity',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=12, null=True),
        ),
    ]

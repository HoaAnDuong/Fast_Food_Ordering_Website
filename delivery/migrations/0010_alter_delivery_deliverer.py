# Generated by Django 4.1.6 on 2023-04-23 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delivery', '0009_deliverer_profile_last_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='deliverer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deliveries', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.1.6 on 2023-04-23 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0010_alter_delivery_deliverer'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='total_length',
            field=models.FloatField(default=0),
        ),
    ]

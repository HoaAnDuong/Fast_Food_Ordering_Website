# Generated by Django 4.1.6 on 2023-04-24 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0013_alter_delivery_point_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='delivery.delivery_status'),
        ),
    ]

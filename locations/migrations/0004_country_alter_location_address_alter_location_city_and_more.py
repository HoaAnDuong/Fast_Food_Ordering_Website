# Generated by Django 4.1.6 on 2023-03-29 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_remove_location_description_remove_location_latitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='location',
            name='postal_code',
            field=models.TextField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='locations.country'),
        ),
    ]

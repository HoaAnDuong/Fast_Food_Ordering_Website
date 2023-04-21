# Generated by Django 4.1.6 on 2023-03-29 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_alter_location_country_delete_country'),
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
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='locations.country'),
        ),
    ]
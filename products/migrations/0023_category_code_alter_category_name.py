# Generated by Django 4.1.6 on 2023-04-21 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_rename_pending_price_product_new_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='code',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.TextField(default='', max_length=100),
        ),
    ]
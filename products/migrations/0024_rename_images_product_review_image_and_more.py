# Generated by Django 4.1.6 on 2023-05-08 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_category_code_alter_category_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product_review',
            old_name='images',
            new_name='image',
        ),
        migrations.AddField(
            model_name='product_report',
            name='title',
            field=models.TextField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='product_review',
            name='title',
            field=models.TextField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='product_report',
            name='report',
            field=models.TextField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='product_review',
            name='review',
            field=models.TextField(blank=True, max_length=2048),
        ),
    ]
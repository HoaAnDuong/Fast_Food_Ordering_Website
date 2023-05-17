# Generated by Django 4.1.6 on 2023-05-09 09:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0024_rename_images_product_review_image_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product_review',
            unique_together={('product', 'author')},
        ),
    ]
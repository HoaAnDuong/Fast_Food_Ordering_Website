# Generated by Django 4.1.6 on 2023-05-15 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_alter_product_review_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='desciption',
            new_name='description',
        ),
    ]

# Generated by Django 4.1.6 on 2023-04-04 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0011_alter_store_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store_status',
            old_name='name',
            new_name='code',
        ),
    ]

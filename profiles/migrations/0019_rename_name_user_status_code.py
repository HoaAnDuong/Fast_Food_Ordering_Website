# Generated by Django 4.1.6 on 2023-04-05 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0018_rename_name_gender_code_profile_current_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_status',
            old_name='name',
            new_name='code',
        ),
    ]
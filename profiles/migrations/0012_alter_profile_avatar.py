# Generated by Django 4.1.6 on 2023-04-02 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_alter_gender_options_alter_profile_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatars/avatar.png', upload_to='avatars/'),
        ),
    ]
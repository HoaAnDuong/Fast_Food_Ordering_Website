# Generated by Django 4.1.6 on 2023-05-18 21:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('moderating', '0003_action_moderator_changelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='moderator_changelog',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.1.6 on 2023-04-04 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_rename_name_delivery_status_code_and_more'),
        ('profiles', '0017_alter_profile_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gender',
            old_name='name',
            new_name='code',
        ),
        migrations.AddField(
            model_name='profile',
            name='current_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orders.order'),
        ),
    ]

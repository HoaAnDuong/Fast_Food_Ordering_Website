# Generated by Django 4.1.6 on 2023-05-18 21:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moderating', '0002_remove_product_complaint_complaint_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Moderator_Changelog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_id', models.BigIntegerField(blank=True, null=True)),
                ('targer_type', models.CharField(default='', max_length=255)),
                ('old_value', models.TextField(default='')),
                ('new_value', models.TextField(default='')),
                ('description', models.TextField(default='', max_length=1024)),
                ('reason', models.TextField(default='', max_length=256)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='moderating.action')),
                ('moderator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changelogs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
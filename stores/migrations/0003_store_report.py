# Generated by Django 4.1.6 on 2023-03-03 02:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stores', '0002_store_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store_Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.store')),
            ],
        ),
    ]

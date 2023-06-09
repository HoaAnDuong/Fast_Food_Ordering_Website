# Generated by Django 4.1.6 on 2023-03-30 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_user_status_alter_profile_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.gender'),
        ),
    ]

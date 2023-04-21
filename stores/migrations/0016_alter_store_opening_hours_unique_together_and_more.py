# Generated by Django 4.1.6 on 2023-04-06 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0015_alter_store_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='store_opening_hours',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='store_opening_hours',
            name='from_hour',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='store_opening_hours',
            name='to_hour',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='store_opening_hours',
            name='weekday',
            field=models.IntegerField(blank=True, choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], null=True),
        ),
        migrations.AlterUniqueTogether(
            name='store_opening_hours',
            unique_together={('store', 'weekday')},
        ),
        migrations.RemoveField(
            model_name='store_opening_hours',
            name='opening_hours',
        ),
        migrations.DeleteModel(
            name='Opening_Hours',
        ),
    ]

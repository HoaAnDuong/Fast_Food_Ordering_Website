# Generated by Django 4.1.6 on 2023-04-07 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_order_moderated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_Method',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orders.payment_method'),
        ),
    ]
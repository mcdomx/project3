# Generated by Django 2.0.7 on 2018-07-31 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.Order_status'),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.0.7 on 2018-08-01 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_auto_20180801_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.ForeignKey(default='Placed', on_delete=django.db.models.deletion.CASCADE, to='orders.Order_status'),
        ),
    ]

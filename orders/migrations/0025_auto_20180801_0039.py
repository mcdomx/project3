# Generated by Django 2.0.7 on 2018-08-01 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_auto_20180801_0035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_status',
            name='id',
        ),
        migrations.AlterField(
            model_name='order_status',
            name='status',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]

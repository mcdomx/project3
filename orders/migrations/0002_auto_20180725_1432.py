# Generated by Django 2.0.7 on 2018-07-25 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu_categories',
            name='id',
        ),
        migrations.AlterField(
            model_name='menu_categories',
            name='category',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]

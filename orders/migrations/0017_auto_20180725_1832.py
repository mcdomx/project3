# Generated by Django 2.0.7 on 2018-07-25 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_sub_addons'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu_items',
            name='allow_sub_addons',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sub_addons',
            name='restricted_menu_item',
            field=models.CharField(max_length=64),
        ),
    ]

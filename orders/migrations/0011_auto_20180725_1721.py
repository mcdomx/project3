# Generated by Django 2.0.7 on 2018-07-25 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_remove_menu_items_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu_items',
            name='category',
            field=models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, to='orders.Menu_categories'),
        ),
    ]

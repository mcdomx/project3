# Generated by Django 2.0.7 on 2018-07-25 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_menu_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu_items',
            name='category',
            field=models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.Menu_categories'),
        ),
    ]

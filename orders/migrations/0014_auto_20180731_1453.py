# Generated by Django 2.0.7 on 2018-07-31 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_menu_items_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_line',
            old_name='sub_addons',
            new_name='addons',
        ),
        migrations.AlterField(
            model_name='order_line',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='orders.Menu_categories'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order_line',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Sizes'),
        ),
        migrations.AlterField(
            model_name='order_line',
            name='toppings',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Toppings'),
        ),
    ]

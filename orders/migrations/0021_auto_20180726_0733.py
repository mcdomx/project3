# Generated by Django 2.0.7 on 2018-07-26 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_order_order_line'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza_toppings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topping', models.CharField(max_length=64)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='order',
            name='lines',
            field=models.ManyToManyField(to='orders.Order_line'),
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='order_line',
            name='menu_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Menu_items'),
        ),
        migrations.AddField(
            model_name='order_line',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='order_line',
            name='size',
            field=models.CharField(blank=True, choices=[('SM', 'small'), ('LG', 'large')], max_length=16),
        ),
        migrations.AddField(
            model_name='order_line',
            name='sub_addons',
            field=models.ManyToManyField(blank=True, to='orders.Sub_addons'),
        ),
        migrations.AddField(
            model_name='order_line',
            name='toppings',
            field=models.CharField(blank=True, choices=[('CHEESE', 'cheese'), ('1', '1 topping'), ('2', '2 toppings'), ('3', '3 toppings'), ('SPECIAL', 'special')], max_length=64),
        ),
        migrations.AddField(
            model_name='order_line',
            name='topping_items',
            field=models.ManyToManyField(blank=True, to='orders.Pizza_toppings'),
        ),
    ]
# Generated by Django 2.0.7 on 2018-07-25 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20180725_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu_items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=64)),
                ('available', models.BooleanField(default=True)),
                ('size', models.CharField(choices=[('SM', 'small'), ('LG', 'large')], max_length=16)),
                ('toppings', models.CharField(choices=[('CHEESE', 'cheese'), ('1', '1 topping'), ('2', '2 toppings'), ('3', '3 toppings'), ('SPECIAL', 'special')], max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='orders.Menu_categories')),
            ],
        ),
    ]

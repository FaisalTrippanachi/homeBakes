# Generated by Django 4.2 on 2023-04-21 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeBake', '0002_cart_delivery_date_cart_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='order_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='order_no',
            field=models.CharField(default='', max_length=50),
        ),
    ]
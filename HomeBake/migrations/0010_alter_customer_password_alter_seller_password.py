# Generated by Django 4.2.3 on 2023-07-18 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeBake', '0009_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='seller',
            name='password',
            field=models.CharField(max_length=300),
        ),
    ]
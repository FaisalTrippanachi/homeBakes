# Generated by Django 4.2 on 2023-07-31 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeBake', '0014_merge_20230731_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='first_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='seller',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
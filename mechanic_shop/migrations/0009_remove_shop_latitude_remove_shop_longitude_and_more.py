# Generated by Django 5.0.2 on 2024-03-30 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mechanic_shop', '0008_alter_shop_latitude_alter_shop_longitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='shop_location',
        ),
    ]

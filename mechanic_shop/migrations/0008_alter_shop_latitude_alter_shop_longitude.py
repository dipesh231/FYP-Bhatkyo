# Generated by Django 5.0.2 on 2024-03-28 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechanic_shop', '0007_alter_shop_latitude_alter_shop_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='latitude',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='longitude',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

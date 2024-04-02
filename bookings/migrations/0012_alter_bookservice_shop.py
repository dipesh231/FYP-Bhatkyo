# Generated by Django 5.0.2 on 2024-04-01 14:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0011_alter_bookservice_date'),
        ('mechanic_shop', '0011_delete_servicebill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookservice',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mechanic_shop.service'),
        ),
    ]
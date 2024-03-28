# Generated by Django 5.0.2 on 2024-03-05 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechanic_shop', '0004_alter_shop_vehicles'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='verification_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('verified', 'Verified')], default='pending', max_length=20),
        ),
    ]
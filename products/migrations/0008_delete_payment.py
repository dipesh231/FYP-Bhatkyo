# Generated by Django 5.0.2 on 2024-04-01 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_payment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]

# Generated by Django 5.0.2 on 2024-03-03 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechanic_shop', '0002_alter_shop_shop_lisence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='vehicles',
            field=models.CharField(choices=[('two_wheelers', 'Two Wheelers'), ('four_wheelers', 'Four Wheelers')], max_length=100),
        ),
    ]

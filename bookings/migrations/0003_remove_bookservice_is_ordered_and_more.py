# Generated by Django 5.0.2 on 2024-03-10 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_alter_bookservice_services_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookservice',
            name='is_ordered',
        ),
        migrations.AlterField(
            model_name='bookservice',
            name='vehicles',
            field=models.CharField(choices=[('two_wheelers', 'Two Wheelers'), ('four_wheelers', 'Four Wheelers'), ('both', 'Both')], max_length=100, null=True),
        ),
    ]

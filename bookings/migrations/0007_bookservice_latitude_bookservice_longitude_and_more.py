# Generated by Django 5.0.2 on 2024-04-01 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_bookservice_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookservice',
            name='latitude',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='bookservice',
            name='longitude',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='bookservice',
            name='location',
            field=models.CharField(null=True),
        ),
    ]
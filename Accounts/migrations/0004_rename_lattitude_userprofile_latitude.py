# Generated by Django 5.0.2 on 2024-03-30 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='lattitude',
            new_name='latitude',
        ),
    ]

# Generated by Django 3.1.7 on 2021-03-26 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_drop_channels'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='channels_json',
            new_name='channels',
        ),
    ]

# Generated by Django 3.1.13 on 2021-09-19 23:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0007_add_content_type_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='notifs_notifications',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
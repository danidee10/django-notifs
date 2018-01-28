"""Celery init."""

from __future__ import absolute_import, unicode_literals
import os

import django

from celery import Celery

django.setup()  # This is key


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifs.settings')

app = Celery('notifs')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

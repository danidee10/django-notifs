"""Celery init."""

from __future__ import absolute_import, unicode_literals
import os

from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifs.settings')

app = Celery('notifs')
app.config_from_object('django.conf:settings', namespace='CELERY')
from notifications import tasks


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

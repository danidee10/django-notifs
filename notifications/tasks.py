"""Celery tasks."""

from __future__ import absolute_import, unicode_literals
from celery import shared_task

from .utils import import_channel


@shared_task
def send_notification(notification):
    """Send notification via a channel to celery."""
    for channel_alias in notification['channels']:
        channel = import_channel(channel_alias)(**notification)

        message = channel.construct_message()
        channel.notify(message)

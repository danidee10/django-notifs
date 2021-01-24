"""Celery tasks."""

from __future__ import absolute_import, unicode_literals
import importlib

from celery import shared_task

from . import default_settings as settings


def __validate_channel_alias(channel_alias):
    """
    Validates a channel alias against settings.NOTIFICATION_CHANNELS.

    returns the channel's path (i.e the path to the Channel's class)
    raises an AttributeError for invalid aliases
    """
    try:
        channel_path = settings.NOTIFICATIONS_CHANNELS[channel_alias]
    except KeyError:
        raise AttributeError(
            '"%s" is not a valid delivery channel alias. '
            'Check your applications settings for NOTIFICATIONS_CHANNELS'
            % channel_alias
        )

    return channel_path


def __import_channel(channel_path):
    """helper to import channel classes from string paths."""
    package, attr = channel_path.rsplit('.', 1)

    return getattr(importlib.import_module(package), attr)


@shared_task
def send_notification(notification):
    """Send notification via a channel to celery."""
    for channel_alias in notification['channels']:
        # Validate channel alias
        channel_path = __validate_channel_alias(channel_alias)

        channel = __import_channel(channel_path)(**notification)

        message = channel.construct_message()
        channel.notify(message)

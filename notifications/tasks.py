"""Celery tasks."""

from __future__ import absolute_import, unicode_literals
import importlib

from celery import shared_task

from . import default_settings as settings


def _import_channel(channel_alias):
    """
    helper to import channels aliases from string paths.

    raises an AttributeError if a channel can't be found by it's alias
    """
    try:
        channel_path = settings.NOTIFICATIONS_CHANNELS[channel_alias]
    except KeyError:
        raise AttributeError(
            '"%s" is not a valid delivery channel alias. '
            'Check your applications settings for NOTIFICATIONS_CHANNELS'
            % channel_alias
        )
    package, attr = channel_path.rsplit('.', 1)

    return getattr(importlib.import_module(package), attr)


@shared_task
def send_notification(notification):
    """Send notification via a channel to celery."""
    for channel_alias in notification['channels']:
        channel = _import_channel(channel_alias)(**notification)

        message = channel.construct_message()
        channel.notify(message)

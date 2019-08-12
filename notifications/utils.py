"""Utilities and helper functions."""

import importlib

from . import NotificationError
from .models import Notification
from . import default_settings as settings


def import_channel(channel_alias):
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


def notify(silent=False, **kwargs):
    """Helper method to send a notification."""
    from .tasks import send_notification

    notification = Notification(**kwargs)

    # If it's a not a silent notification, save the notification
    if not silent:
        notification.save()

    # Send the notification asynchronously with celery
    send_notification.delay(notification.to_json())


def read(notify_id, recipient):
    """
    Helper method to read a notification.

    Raises NotificationError if the user doesn't have access
    to read the notification
    """
    notification = Notification.objects.get(id=notify_id)

    if recipient != notification.recipient:
        raise NotificationError('You cannot read this notification')

    notification.read()

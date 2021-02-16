"""Utilities and helper functions."""

import importlib

from . import NotificationError
from .models import Notification
from . import default_settings as settings


def notify(silent=False, **kwargs):
    """Helper method to send a notification."""
    notification = Notification(**kwargs)

    # Validate channels
    for channel_alias in notification.channels:
        _validate_channel_alias(channel_alias)

    # If it's a not a silent notification, save the notification
    if not silent:
        notification.save()

    # Send the notification asynchronously with celery
    notification_delivery_backend = _import_class_string(
        settings.NOTIFICATIONS_DELIVERY_BACKEND
    )
    notification_delivery_backend(notification).run()


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


def _validate_channel_alias(channel_alias):
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


def _import_class_string(path):
    """helper to import classes from string paths."""
    package, attr = path.rsplit('.', 1)

    return getattr(importlib.import_module(package), attr)

"""Utilities and helper functions."""

import importlib

from django.conf import settings as django_settings

from . import NotificationError
from . import default_settings as settings


def notify(*notifications, countdown=0):
    """Helper method to send multiple notifications."""
    for notification in notifications:
        notification.notify(countdown)


def read(notify_id, recipient):
    """
    Helper method to read a notification.

    Raises NotificationError if the user doesn't have access
    to read the notification
    """
    Notification = get_notification_model()
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


def get_notification_model():
    notification_model_path = getattr(
        django_settings, 'NOTIFICATIONS_MODEL', 'notifications.models.Notification'
    )
    return _import_class_string(notification_model_path)

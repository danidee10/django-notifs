"""Utilities and helper functions."""

import importlib

from django.conf import settings as django_settings

from . import NotificationError
from . import default_settings as settings


def notify(silent=False, countdown=0, **kwargs):
    """Helper method to send multiple notifications."""
    Notification = get_notification_model()
    notification = Notification(**kwargs)

    # Validate channels
    validated_channels = []
    for name in notification.channels:
        channel_path = _validate_channel_name(name)
        validated_channels.append(channel_path)

    # If it's a not a silent notification, save the notification
    if not silent:
        notification.save()

    # Send the notifications asynchronously
    context = notification.extra_data.pop('context', {})
    for channel_path in validated_channels:
        notification_channel = _import_class_string(channel_path)(notification, context=context)
        notification_channel.notify(countdown)


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


def _validate_channel_name(name):
    """
    Validates a channel alias against settings.NOTIFICATION_CHANNELS.

    returns the channel's path (i.e the path to the Channel's class)
    raises an AttributeError for invalid aliases
    """
    from notifications.channels import BaseNotificationChannel

    try:
        channel_path = BaseNotificationChannel.registered_channels[name]
    except KeyError:
        raise AttributeError(
            '"%s" is not a valid delivery channel alias. '
            'Ensure that the Notification was registered properly'
            % name
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

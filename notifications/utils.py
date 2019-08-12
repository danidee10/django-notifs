"""Utilities and helper functions."""

from . import NotificationError
from .models import Notification
from .tasks import send_notification


def notify(silent=False, **kwargs):
    """Helper method to send a notification."""
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

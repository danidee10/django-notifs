"""Defines and listens to notification signals."""

import importlib

from django.dispatch import Signal, receiver

import notifs.default_settings as settings

from . import NotificationError
from .models import Notification


notify = Signal(providing_args=(
    'source', 'source_display_name', 'recipient', 'action', 'category' 'obj',
    'url', 'short_description', 'extra_data', 'silent'
))
read = Signal(providing_args=('notify_id', 'recipient'))


def import_attr(path):
    """helper to import classes/attributes from str paths."""
    package, attr = path.rsplit('.', 1)

    return getattr(importlib.import_module(package), attr)


@receiver(notify)
def create_notification(**kwargs):
    """Notify signal receiver."""
    # make fresh copy and retain kwargs
    params = kwargs.copy()
    del params['signal']
    del params['sender']
    try:
        del params['silent']
    except KeyError:
        pass

    # If it's a not a silent notification create the notification
    if not kwargs.get('silent', False):
        Notification.objects.create(**params)

    # send via custom adapters
    for channel_path in settings.NOTIFICATIONS_CHANNELS:
        channel = import_attr(channel_path)(**params)

        message = channel.construct_message()
        channel.notify(message)


@receiver(read)
def read_notification(**kwargs):
    """
    Mark notification as read.

    Raises NotificationError if the user doesn't have access
    to read the notification
    """
    notify_id = kwargs['notify_id']
    recipient = kwargs['recipient']
    notification = Notification.objects.get(id=notify_id)

    if recipient != notification.recipient:
        raise NotificationError('You cannot read this notification')

    notification.read()

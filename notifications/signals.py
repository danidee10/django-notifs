"""Defines and listens to notification signals."""

import importlib

from django.dispatch import Signal, receiver
from django.conf import settings

from .models import Notification

notify = Signal(providing_args=('user', 'actor', 'action' 'obj', 'url'))
read = Signal(providing_args=('notify_id'))


def import_attr(path):
    """helper to import classes/attributes from str paths."""
    package, attr = path.rsplit('.', 1)

    return getattr(importlib.import_module(package), attr)

@receiver(notify)
def create_notification(sender, **kwargs):
    """Notify signal receiver."""
    # make fresh copy and retain kwargs
    params = kwargs.copy()
    del params['signal']

    Notification.objects.create(**params)

    # send via custom adapters
    for adapter_path in settings.NOTIFICATION_ADAPTERS:
        adapter = import_attr(adapter_path)
        adapter(**kwargs).notify()

@receiver(read)
def read_notification(sender, **kwargs):
    """Mark notification as read."""
    notify_id = kwargs['notify_id']
    notify_obj = Notification.objects.get(id=notify_id)
    notify_obj.read()

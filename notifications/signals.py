"""Defines and listens to notification signals."""

from django.dispatch import Signal, receiver

from . import NotificationError
from .models import Notification
from .tasks import send_notification


notify = Signal(providing_args=(
    'source', 'source_display_name', 'recipient', 'action', 'category' 'obj',
    'url', 'short_description', 'extra_data', 'silent', 'channels'
))
read = Signal(providing_args=('notify_id', 'recipient'))


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

    notification = Notification(**params)

    # If it's a not a silent notification, save the notification
    if not kwargs.get('silent', False):
        notification.save()

    # Send the notification asynchronously with celery
    send_notification.delay(notification.to_json())


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

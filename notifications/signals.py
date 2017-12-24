"""Defines and listens to notification signals."""

import importlib
from json import dumps

import pika

from django.conf import settings
from django.dispatch import Signal, receiver

from . import NotificationError
from .models import Notification


notify = Signal(providing_args=('user', 'actor', 'action' 'obj', 'url'))
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

    notification = Notification.objects.create(**params)

    # send via custom adapters
    for adapter_path in getattr(settings, 'NOTIFICATION_ADAPTERS', []):
        adapter = import_attr(adapter_path)
        adapter(**kwargs).notify()

    if getattr(settings, 'NOTIFICATIONS_WEBSOCKET', False):
        send_to_queue(notification)


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


def send_to_queue(notification):
    """
    Puts a new message on the queue.
    
    The queue is named after the username (for Uniqueness)
    """
    rabbit_mq_url = getattr(
        settings, 'NOTIFICATIONS_RABBIT_MQ_URL', 'amqp://guest:guest@localhost:5672'
    )
    connection = pika.BlockingConnection(
        pika.connection.URLParameters(rabbit_mq_url)
    )
    channel = connection.channel()

    channel.queue_declare(queue=notification.source.username)

    channel.confirm_delivery()

    jsonified_messasge = dumps(notification.to_json())
    published = channel.basic_publish(
        exchange='', routing_key=notification.recipient.username,
        body=jsonified_messasge
    )

    if published:
        print("Sent '{}'".format(jsonified_messasge))
    else:
        print('Message was not delivered')

    connection.close()

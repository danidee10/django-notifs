"""Base Implementation of a Delivery Backend."""

import abc
from json import dumps

import pika

from django.contrib.auth import get_user_model

from .models import Notification
from . import default_settings as settings


class BaseNotificationChannel(metaclass=abc.ABCMeta):
    """Base channel for sending notifications."""

    def __init__(self, **kwargs):
        self.notification_kwargs = kwargs

    @abc.abstractmethod
    def construct_message(self):
        """Constructs a message from notification details."""
        pass

    @abc.abstractmethod
    def notify(self, message):
        """Sends the notification."""
        pass


class ConsoleChannel(BaseNotificationChannel):
    """Dummy channel that prints to the console."""

    def construct_message(self):
        """Stringify the notification kwargs."""
        return str(self.notification_kwargs)

    def notify(self, message):
        print(message)


class BasicWebSocketChannel(BaseNotificationChannel):
    """It creates a RabbitMQ user for each user (based on their username)."""

    def _connect(self):
        """Connect to the RabbitMQ Server."""
        rabbit_mq_url = settings.NOTIFICATIONS_RABBIT_MQ_URL
        connection = pika.BlockingConnection(
            pika.connection.URLParameters(rabbit_mq_url)
        )

        return connection

    def construct_message(self):
        """Construct message from notification details."""
        
        return self.notification_kwargs

    def notify(self, message):
        """
        Puts a new message on the queue.
        
        The queue is named based on the username (for Uniqueness)
        """
        connection = self._connect()
        channel = connection.channel()

        # Get user instance
        User = get_user_model()
        source = User.objects.get(id=message['source'])
        recipient = User.objects.get(id=message['recipient'])

        channel.queue_declare(queue=source.username)

        jsonified_messasge = dumps(message)
        channel.basic_publish(
            exchange='', routing_key=recipient.username,
            body=jsonified_messasge
        )

        connection.close()

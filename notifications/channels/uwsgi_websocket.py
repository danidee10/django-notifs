"""Base Implementation of a Delivery Backend."""

from json import dumps

import pika

from django.contrib.auth import get_user_model

from .base import BaseNotificationChannel
from notifications import default_settings as settings


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

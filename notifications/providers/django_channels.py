"""Notification channels for django-notifs."""

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .base import BaseNotificationProvider


class DjangoChannelsNotificationProvider(BaseNotificationProvider):
    """django-channels websocket provider"""

    name = 'django_channels'

    @property
    def channel_layer(self):
        return get_channel_layer(self.context['channel_layer'])

    @property
    def destination(self):
        return self.context['destination']

    def send(self, payload):
        async_to_sync(self.channel_layer.group_send)(self.destination, payload)

    def send_bulk(self, payloads):
        for payload in payloads:
            self.send(payload)

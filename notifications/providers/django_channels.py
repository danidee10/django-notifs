"""Notification channels for django-notifs."""

from notifications import ImproperlyInstalledNotificationProvider

try:
    from channels.layers import get_channel_layer
except ImportError:
    raise ImproperlyInstalledNotificationProvider(
        missing_package='channels', provider='django_channels'
    )

from asgiref.sync import async_to_sync
from pydantic import BaseModel

from .base import BaseNotificationProvider


class DjangoChannelsSchema(BaseModel):
    type: str
    """settings.NOTIFICATIONS_WEBSOCKET_EVENT_NAME or a custom event name"""

    message: str


class DjangoChannelsNotificationProvider(BaseNotificationProvider):
    """django-channels websocket provider"""

    name = 'django_channels'

    @property
    def channel_layer(self):
        return get_channel_layer(self.context.get('channel_layer', 'default'))

    @property
    def destination(self):
        return self.context['destination']

    def get_validator(self):
        return DjangoChannelsSchema

    def send(self, payload):
        async_to_sync(self.channel_layer.group_send)(self.destination, payload)

    def send_bulk(self, payloads):
        for payload in payloads:
            self.send(payload)

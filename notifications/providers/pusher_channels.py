from typing import Dict

from notifications import ImproperlyInstalledNotificationProvider

try:
    from pusher import Pusher
except ImportError:
    raise ImproperlyInstalledNotificationProvider(
        missing_package='pusher', provider='pusher_channels'
    )

from pydantic import BaseModel, Field

from notifications import default_settings as settings

from . import BaseNotificationProvider


class PusherChannelsSchema(BaseModel):
    channel: str = Field(description='The pusher channel name')
    name: str = Field(description='The event name')
    data: Dict = Field(description='The message data')


class PusherChannelsNotificationProvider(BaseNotificationProvider):
    name = 'pusher_channels'
    validator = PusherChannelsSchema

    def __init__(self, context=dict()):
        self.pusher_client = Pusher.from_url(settings.NOTIFICATIONS_PUSHER_CHANNELS_URL)
        super().__init__(context=context)

    def send(self, payload):
        self.pusher_client.trigger(**payload)

    def send_bulk(self, payloads):
        self.pusher_client.trigger_batch(payloads)

from typing import Dict, List, Union

try:
    from pusher import Pusher

    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False

from pydantic import BaseModel, Field

from notifications import default_settings as settings

from . import BaseNotificationProvider


class PusherChannelsSchema(BaseModel):
    channels: Union[str, List] = Field(description='The pusher channel name')
    event_name: str = Field(description='The event name')
    data: Dict = Field(description='The message data')


class PusherChannelsNotificationProvider(BaseNotificationProvider):
    name = 'pusher_channels'
    validator = PusherChannelsSchema
    package = 'pusher'

    HAS_DEPENDENCIES = HAS_DEPENDENCIES

    def __init__(self, context=dict()):
        super().__init__(context=context)
        self.pusher_client = Pusher.from_url(settings.NOTIFICATIONS_PUSHER_CHANNELS_URL)

    def send(self, payload):
        return self.pusher_client.trigger(**payload)

    def send_bulk(self, payloads):
        return self.pusher_client.trigger_batch(payloads)

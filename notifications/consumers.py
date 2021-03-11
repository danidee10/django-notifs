"""Channels consumers."""

import json
import logging

from channels.consumer import SyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from . import default_settings as settings
from notifications.backends.utils import _send_notification


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('django_notifs.backends.channels')


class DjangoNotifsConsumer(SyncConsumer):

    def notify(self, message):
        _send_notification(
            message['notification'], message['channel_alias'], logger
        )


class DjangoNotifsWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs'][
            settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM
        ]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Leave the group."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from the WebSocket

        for bi-directional communication)
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': settings.NOTIFICATIONS_WEBSOCKET_EVENT_NAME,
                'message': message
            }
        )


async def __websocket_message(self, event):
    """Receive messages from the group."""
    message = event['message']

    # Send message to WebSocket
    await self.send(message)


setattr(
    DjangoNotifsWebsocketConsumer,
    settings.NOTIFICATIONS_WEBSOCKET_EVENT_NAME, __websocket_message
)

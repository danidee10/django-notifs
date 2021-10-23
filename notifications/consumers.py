"""Channels consumers."""

import asyncio
import json
import logging

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from notifications.backends.django_channels import ChannelsBackend

from . import default_settings as settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('django_notifs.backends.channels')


class DjangoNotifsConsumer(AsyncConsumer):
    """
    This class inherits from AsyncConsumer

    so we can delay (`sleep`) multiple messages
    """

    async def notify(self, message):
        await asyncio.sleep(message['countdown'])

        await database_sync_to_async(ChannelsBackend.consume)(
            message['provider'],
            message['payload'],
            message['context'],
        )


class DjangoNotifsWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs'][
            settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM
        ]

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """Leave the group."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Receive message from the WebSocket

        for bi-directional communication)
        """
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', {})

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': settings.NOTIFICATIONS_WEBSOCKET_EVENT_NAME,
                'message': message,
            },
        )


async def __websocket_message(self, event):
    """Receive messages from the group."""
    message = event['message']
    await self.send(message)


setattr(
    DjangoNotifsWebsocketConsumer,
    settings.NOTIFICATIONS_WEBSOCKET_EVENT_NAME,
    __websocket_message,
)

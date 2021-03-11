"""Notification channels for django-notifs."""

from json import dumps

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .base import BaseNotificationChannel
from .. import default_settings as settings


class WebSocketChannel(BaseNotificationChannel):
    """django-channels websocket channel"""

    destination_name = settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM

    def _validate_notification_kwargs(self):
        notif_kwargs = self.notification_kwargs

        try:
            notif_kwargs['extra_data'][self.destination_name]
        except KeyError:
            raise KeyError(
                f'`extra_kwargs` must contain the `{self.destination_name}`'
                'key'
            )

    def construct_message(self):
        """Construct the message to be sent."""
        self._validate_notification_kwargs()

        extra_data = self.notification_kwargs['extra_data']

        return dumps(extra_data['message'])

    def notify(self, message):
        channel_layer = get_channel_layer()
        destination = self.notification_kwargs['extra_data'][
            self.destination_name
        ]

        async_to_sync(channel_layer.group_send)(
            destination,
            {
                'type': settings.NOTIFICATIONS_WEBSOCKET_EVENT_NAME,
                'message': message
            }
        )

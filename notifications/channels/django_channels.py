"""Notification channels for django-notifs."""

import json
from notifications import default_settings as settings
from notifications.channels import BaseNotificationChannel


class DjangoWebSocketChannel(BaseNotificationChannel):
    """django-channels websocket channel"""

    name = 'websocket'
    providers = ['django_channels']

    def build_payload(self, provider):
        return {
            'type': settings.NOTIFICATIONS_WEBSOCKET_EVENT_NAME,
            'message': json.dumps(self.context['message']),
        }

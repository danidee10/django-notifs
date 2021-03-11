"""Default settings for django-notifs project."""

from django.conf import settings


NOTIFICATIONS_DELIVERY_BACKEND = getattr(
    settings, 'NOTIFICATIONS_DELIVERY_BACKEND',
    'notifications.backends.Synchronous'
)

NOTIFICATIONS_QUEUE_NAME = getattr(
    settings, 'NOTIFICATIONS_QUEUE_NAME', 'django_notifs'
)

NOTIFICATIONS_RETRY = getattr(settings, 'NOTIFICATIONS_RETRY', False)

NOTIFICATIONS_RETRY_INTERVAL = getattr(
    settings, 'NOTIFICATIONS_RETRY_INTERVAL', 5
)

NOTIFICATIONS_MAX_RETRIES = getattr(settings, 'NOTIFICATIONS_MAX_RETRIES', 5)

NOTIFICATIONS_CHANNELS = getattr(settings, 'NOTIFICATIONS_CHANNELS', {})

NOTIFICATIONS_WEBSOCKET_EVENT_NAME = getattr(
    settings, 'NOTIFICATIONS_WEBSOCKET_EVENT_NAME', 'notifs_websocket_message'
)
NOTIFICATIONS_WEBSOCKET_URL_PARAM = getattr(
    settings, 'NOTIFICATIONS_WEBSOCKET_URL_PARAM', 'room_name'
)

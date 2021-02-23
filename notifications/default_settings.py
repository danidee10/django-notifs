"""Default settings for django-notifs project."""

from django.conf import settings


NOTIFICATIONS_USE_WEBSOCKET = getattr(
    settings, 'NOTIFICATIONS_USE_WEBSOCKET', False
)

NOTIFICATIONS_RABBIT_MQ_URL = getattr(
    settings, 'NOTIFICATIONS_RABBIT_MQ_URL',
    'amqp://guest:guest@localhost:5672'
)

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

if NOTIFICATIONS_USE_WEBSOCKET:
    NOTIFICATIONS_CHANNELS['websocket'] = \
        'notifications.channels.BasicWebSocketChannel'

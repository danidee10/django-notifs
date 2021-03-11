"""Django channels routes."""

from django.urls import path

from . import default_settings as settings
from .consumers import DjangoNotifsWebsocketConsumer

websocket_urlpatterns = [
    path(
        f'<{settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM}>',
        DjangoNotifsWebsocketConsumer.as_asgi()
    )
]

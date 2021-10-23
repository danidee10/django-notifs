from notifications import ImproperlyInstalledNotificationProvider

try:
    from pusher import Pusher
except ImportError:
    raise ImproperlyInstalledNotificationProvider(
        missing_package='pusher', provider='pusher_channels'
    )

from notifications import default_settings as settings

from . import BaseNotificationProvider


class PusherChannelsNotificationProvider(BaseNotificationProvider):
    name = 'pusher_channels'

    def __init__(self, context=dict()):
        self.pusher_client = Pusher.from_url(settings.NOTIFICATIONS_PUSHER_CHANNELS_URL)
        super().__init__(context=context)

    def send(self, payload):
        self.pusher_client.trigger(**payload)

    def send_bulk(self, payloads):
        self.pusher_client.trigger_batch(payloads)

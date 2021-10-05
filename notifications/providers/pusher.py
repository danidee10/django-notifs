from . import BaseNotificationProvider

from notifications import default_settings as settings

from pusher import Pusher


class PusherNotificationProvider(BaseNotificationProvider):
    name = 'pusher'

    def __init__(self, context=dict()):
        self.pusher_client = Pusher.from_url(settings.NOTIFICATIONS_PUSHER_URL)
        super().__init__(context=context)

    def send(self, payload):
        self.pusher_client.trigger(**payload)

    def send_bulk(self, payloads):
        self.pusher_client.trigger_batch(payloads)

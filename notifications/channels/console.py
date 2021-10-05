from .base import BaseNotificationChannel


class ConsoleNotificationChannel(BaseNotificationChannel):
    name = 'console'
    providers = ['console']

    def build_payload(self, provider):
        return {'context': self.context, 'payload': provider}

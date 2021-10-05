from . import BaseNotificationProvider


class ConsoleNotificationProvider(BaseNotificationProvider):
    """Dummy provider that prints to the console."""

    name = 'console'

    def send(self, payload):
        print(payload)

    def send_bulk(self, payloads):
        for payload in payloads:
            self.send(payload)

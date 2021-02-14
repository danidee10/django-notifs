from .base import BaseNotificationChannel


class ConsoleChannel(BaseNotificationChannel):
    """Dummy channel that prints to the console."""

    def construct_message(self):
        """Stringify the notification kwargs."""
        return str(self.notification_kwargs)

    def notify(self, message):
        print(message)

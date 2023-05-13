from typing import List
from notifications.channels import BaseNotificationChannel


class Group(BaseNotificationChannel):
    def __init__(self, *notification_channels: List[BaseNotificationChannel]):
        self.notification_channels = notification_channels

    def build_payload(self, provider):
        """Constructs a paylod from the notification object."""
        return [
            channel.build_payload(provider) for channel in self.notification_channels
        ]

    def notify(self, countdown=0):
        delivery_backend = self.get_delivery_backend()
        delivery_backend(self).run(countdown)

    def run(self):
        pass

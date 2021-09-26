from notifications.channels import BaseNotificationChannel


class ConsoleNotificationChannel(BaseNotificationChannel):
    name = 'console'
    providers = ['console']

    def build_payload(self, provider):
        return provider

from slack_sdk import WebClient

from notifications import default_settings as settings

from . import BaseNotificationProvider


class SlackNotificationProvider(BaseNotificationProvider):
    name = 'slack'

    def __init__(self, context=dict()):
        self.slack_client = WebClient(token=settings.NOTIFICATIONS_SLACK_BOT_TOKEN)
        super().__init__(context=context)

    def send(self, payload):
        self.slack_client.chat_postMessage(**payload)

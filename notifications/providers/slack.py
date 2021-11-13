try:
    from slack_sdk import WebClient

    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False

from pydantic import BaseModel, Field

from notifications import default_settings as settings

from . import BaseNotificationProvider


class SlackSchema(BaseModel):
    channel: str = Field(description='The #slack-channel-name')
    text: str = Field(description='The message body')


class SlackNotificationProvider(BaseNotificationProvider):
    name = 'slack'
    validator = SlackSchema
    package = 'slack_sdk'

    HAS_DEPENDENCIES = HAS_DEPENDENCIES

    def __init__(self, context=dict()):
        super().__init__(context=context)
        self.slack_client = WebClient(token=settings.NOTIFICATIONS_SLACK_BOT_TOKEN)

    def send(self, payload):
        return self.slack_client.chat_postMessage(**payload)

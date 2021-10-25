from notifications import ImproperlyInstalledNotificationProvider

try:
    from slack_sdk import WebClient
except ImportError as err:
    raise ImproperlyInstalledNotificationProvider(
        missing_package='slack_sdk', provider='slack'
    ) from err

from pydantic import BaseModel, Field

from notifications import default_settings as settings

from . import BaseNotificationProvider


class SlackSchema(BaseModel):
    channel: str = Field(description=' The #slack-channel-name')
    text: str = Field(description='The message body')


class SlackNotificationProvider(BaseNotificationProvider):
    name = 'slack'
    validator = SlackSchema

    def __init__(self, context=dict()):
        self.slack_client = WebClient(token=settings.NOTIFICATIONS_SLACK_BOT_TOKEN)
        super().__init__(context=context)

    def send(self, payload):
        self.slack_client.chat_postMessage(**payload)

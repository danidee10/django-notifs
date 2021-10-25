from typing import List

from pydantic import BaseModel, Field

from notifications import ImproperlyInstalledNotificationProvider

try:
    from sms import Message, get_connection
except ImportError:
    raise ImproperlyInstalledNotificationProvider(
        missing_package='django_sms', provider='sms'
    )

from . import BaseNotificationProvider


class DjangoSmsSchema(BaseModel):
    body: str = Field(description='The message body')
    originator: str = Field(description='The originating phone number')
    recipients: List[str] = Field(description='The list of recipient phone numbers')


class DjangoSMSNotificationProvider(BaseNotificationProvider):
    name = 'django_sms'
    validator = DjangoSmsSchema

    @staticmethod
    def _get_sms_message(payload):
        message = Message()
        for key, value in payload.items():
            setattr(message, key, value)

        return message

    def send(self, payload):
        sms_message = self._get_sms_message(payload)
        sms_message.send()

    def send_bulk(self, payloads):
        messages = (self._get_sms_message(payload) for payload in payloads)
        connection = get_connection()
        connection.send_messages(messages)

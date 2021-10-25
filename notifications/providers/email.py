from typing import Dict, List, Optional

from django.core.mail import EmailMessage, get_connection
from pydantic import BaseModel, Field

from . import BaseNotificationProvider


class EmailSchema(BaseModel):
    subject: str = Field(description='The subject line of the email')
    body: str = Field(description='The body text. This should be a plain text message')
    to: List[str] = Field(description='A list or tuple of recipient addresses')

    bcc: Optional[List[str]] = Field(
        default=[],
        description="A list or tuple of recipient addresses used in the 'cc'"
        'header when sending the email',
    )
    from_email: Optional[str] = Field(description="The sender's address")
    attachments: Optional[List] = Field(
        default=[],
        description='A list of attachments to put on the message',
    )
    headers: Optional[Dict] = Field(
        default={}, description='A dictionary of extra headers to put on the message'
    )
    reply_to: Optional[List[str]] = Field(
        default=[],
        description="A list or tuple of recipient addresses used in the 'Reply-To'"
        'header when sending the email',
    )


class EmailNotificationProvider(BaseNotificationProvider):
    name = 'email'
    validator = EmailSchema

    @staticmethod
    def _get_email_message(payload):
        message = EmailMessage()
        for key, value in payload.items():
            setattr(message, key, value)

        return message

    def send(self, payload):
        email_message = self._get_email_message(payload)
        email_message.send()

    def send_bulk(self, payloads):
        messages = (self._get_email_message(payload) for payload in payloads)
        connection = get_connection()
        connection.send_messages(messages)

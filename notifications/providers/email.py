from . import BaseNotificationProvider

from django.core.mail import EmailMessage, get_connection


class EmailNotificationProvider(BaseNotificationProvider):
    name = 'email'

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

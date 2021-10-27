from django.test import SimpleTestCase, override_settings

from notifications.channels import BaseNotificationChannel


class EmailNotificationChannel(BaseNotificationChannel):
    name = 'email_notification_channel'
    providers = ['email']

    def build_payload(self, provider):
        payload = {'subject': 'Hello', 'body': 'Hello', 'to': ['example@example.com']}
        if self.context.get('bulk', False) is True:
            return [payload]

        return payload


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class TestEmailProvider(SimpleTestCase):
    def test_email_channels(self):
        email_notification_channel = EmailNotificationChannel({})
        email_notification_channel.notify()

    def test_email_channels_bulk(self):
        email_notification_channel = EmailNotificationChannel(
            {}, context={'bulk': True}
        )
        email_notification_channel.notify()

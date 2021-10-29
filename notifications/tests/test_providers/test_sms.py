from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from notifications.channels import BaseNotificationChannel
from notifications.exceptions import ImproperlyInstalledNotificationProvider


class SMSNotificationChannel(BaseNotificationChannel):
    name = 'sms_notification_channel'
    providers = ['django_sms']

    def build_payload(self, provider):
        payload = {
            'body': 'Hello world',
            'originator': '+15075788089',
            'recipients': ['+1348160307160'],
        }
        if self.context.get('bulk', False) is True:
            return [payload]

        return payload


@override_settings(SMS_BACKEND='sms.backends.locmem.SmsBackend')
class TestSMSProvider(SimpleTestCase):
    @patch(
        'notifications.providers.DjangoSMSNotificationProvider.HAS_DEPENDENCIES',
        False,
    )
    def test_sms_dependency(self):
        slack_notification_channel = SMSNotificationChannel({})

        with self.assertRaises(ImproperlyInstalledNotificationProvider):
            slack_notification_channel.notify()

    def test_sms_channels(self):
        sms_notification_channel = SMSNotificationChannel({})
        sms_notification_channel.notify()

    def test_sms_channels_bulk(self):
        sms_notification_channel = SMSNotificationChannel({}, context={'bulk': True})
        sms_notification_channel.notify()

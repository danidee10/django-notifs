from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from notifications.channels import BaseNotificationChannel
from notifications.exceptions import ImproperlyInstalledNotificationProvider


class SlackNotificationChannel(BaseNotificationChannel):
    name = 'slack_notification_channel'
    providers = ['slack']

    def build_payload(self, provider):
        payload = {
            'channel': '#general',
            'text': 'Hello world',
        }
        if self.context.get('bulk', False) is True:
            return [payload]

        return payload


class TestSlackProvider(SimpleTestCase):
    @patch('slack_sdk.WebClient.chat_postMessage', Mock())
    @patch('notifications.providers.SlackNotificationProvider.HAS_DEPENDENCIES', False)
    def test_slack_dependency(self):
        slack_notification_channel = SlackNotificationChannel({})

        with self.assertRaises(ImproperlyInstalledNotificationProvider):
            slack_notification_channel.notify()

    @patch('slack_sdk.WebClient.chat_postMessage')
    def test_slack_channels(self, mocked_chat_post_message):
        slack_notification_channel = SlackNotificationChannel({})
        slack_notification_channel.notify()
        mocked_chat_post_message.assert_called_with(
            channel='#general', text='Hello world'
        )

    @patch('slack_sdk.WebClient.chat_postMessage')
    def test_slack_channels_bulk(self, mocked_chat_post_message):
        slack_notification_channel = SlackNotificationChannel(
            {}, context={'bulk': True}
        )
        slack_notification_channel.notify()
        mocked_chat_post_message.assert_called_with(
            channel='#general', text='Hello world'
        )

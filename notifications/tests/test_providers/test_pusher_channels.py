from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from notifications.channels import BaseNotificationChannel
from notifications.exceptions import ImproperlyInstalledNotificationProvider


class PusherNotificationChannel(BaseNotificationChannel):
    name = 'pusher_notification_channel'
    providers = ['pusher_channels']

    def build_payload(self, provider):
        payload = {
            'channels': 'notifications',
            'event_name': 'new',
            'data': {'message': 'Hello world'},
        }
        if self.context.get('bulk', False) is True:
            return [payload]

        return payload


class TestPusherChannelsProvider(SimpleTestCase):
    @patch('pusher.Pusher.trigger', Mock())
    @patch(
        'notifications.providers.PusherChannelsNotificationProvider.HAS_DEPENDENCIES',
        False,
    )
    def test_pusher_dependency(self):
        slack_notification_channel = PusherNotificationChannel({})

        with self.assertRaises(ImproperlyInstalledNotificationProvider):
            slack_notification_channel.notify()

    @patch('pusher.Pusher.trigger')
    def test_pusher_channels(self, mocked_trigger):
        pusher_notification_channel = PusherNotificationChannel({})
        pusher_notification_channel.notify()
        mocked_trigger.assert_called_with(
            channels='notifications', event_name='new', data={'message': 'Hello world'}
        )

    @patch('pusher.Pusher.trigger_batch')
    def test_pusher_channels_bulk(self, mocked_trigger_batch):
        pusher_notification_channel = PusherNotificationChannel(
            {}, context={'bulk': True}
        )
        pusher_notification_channel.notify()
        mocked_trigger_batch.assert_called_with(
            [
                {
                    'channels': 'notifications',
                    'event_name': 'new',
                    'data': {'message': 'Hello world'},
                }
            ]
        )
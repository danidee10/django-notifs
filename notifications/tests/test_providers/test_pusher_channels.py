from unittest.mock import patch

from django.test import SimpleTestCase

from notifications.channels import BaseNotificationChannel
from notifications.exceptions import ImproperlyConfiguredProvider


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
    @patch(
        'notifications.providers.PusherChannelsNotificationProvider.HAS_DEPENDENCIES',
        False,
    )
    def test_pusher_dependency(self):
        pusher_notification_channel = PusherNotificationChannel({})

        with self.assertRaises(ImproperlyConfiguredProvider):
            pusher_notification_channel.notify()

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

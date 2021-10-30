from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from tweepy.errors import Forbidden, TooManyRequests

from notifications.channels import BaseNotificationChannel
from notifications.exceptions import ImproperlyConfiguredProvider


class FakeTweepyResponse:

    status_code = 400
    reason = ''

    @classmethod
    def json(cls):
        return {}


class TwitterStatusUpdateNotificationChannel(BaseNotificationChannel):
    name = 'twitter_status_update_notification_channel'
    providers = ['twitter_status_update']

    def build_payload(self, provider):
        payload = {
            'status': 'Hello world',
            'in_reply_to_status_id': '1234567890',
        }
        if self.context.get('bulk', False) is True:
            return [payload]

        return payload


class TestTwitterStatusUpdateProvider(SimpleTestCase):
    @patch(
        'notifications.providers.TwitterStatusUpdateNotificationProvider.HAS_DEPENDENCIES',  # noqa
        False,
    )
    def test_twitter_status_update_dependency(self):
        twitter_status_update_notification_channel = (
            TwitterStatusUpdateNotificationChannel({})
        )

        with self.assertRaises(ImproperlyConfiguredProvider):
            twitter_status_update_notification_channel.notify()

    @patch('tweepy.API.update_status', Mock(side_effect=Forbidden(FakeTweepyResponse)))
    def test_twitter_status_update_forbidden(self):
        twitter_status_update_notification_channel = (
            TwitterStatusUpdateNotificationChannel({}, context={'bulk': True})
        )

        try:
            twitter_status_update_notification_channel.notify()
        except Forbidden:
            self.fail('Raised Forbidden error')

    @patch(
        'tweepy.API.update_status',
        Mock(side_effect=TooManyRequests(FakeTweepyResponse)),
    )
    def test_twitter_status_update_too_many_requests(self):
        twitter_status_update_notification_channel = (
            TwitterStatusUpdateNotificationChannel({}, context={'bulk': True})
        )

        try:
            twitter_status_update_notification_channel.notify()
        except TooManyRequests:
            self.fail('Raised TooManyRequests error')

    @patch('tweepy.API.update_status')
    def test_twitter_status_update_channels(self, mocked_update_status):
        twitter_status_update_notification_channel = (
            TwitterStatusUpdateNotificationChannel({})
        )
        twitter_status_update_notification_channel.notify()
        mocked_update_status.assert_called_with(
            status='Hello world', in_reply_to_status_id='1234567890'
        )

    @patch('tweepy.API.update_status')
    def test_twitter_status_update_channels_bulk(self, mocked_update_status):
        twitter_status_update_notification_channel = (
            TwitterStatusUpdateNotificationChannel({}, context={'bulk': True})
        )
        twitter_status_update_notification_channel.notify()
        mocked_update_status.assert_called_with(
            status='Hello world', in_reply_to_status_id='1234567890'
        )

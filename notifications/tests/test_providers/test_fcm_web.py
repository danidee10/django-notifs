from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from notifications.channels import BaseNotificationChannel
from notifications.exceptions import ImproperlyConfiguredProvider
from notifications.providers import FCMWebNotificationProvider


class FCMWebNotificationChannel(BaseNotificationChannel):
    name = 'fcm_web_notification_channel'
    providers = ['fcm_web']

    def build_payload(self, provider):
        payload = {
            'registration_id': '12345',
            'message_title': 'Hello',
            'message_body': 'Hello world',
        }
        if self.context.get('bulk', False) is True:
            registration_id = payload.pop('registration_id')
            payload['registration_ids'] = [registration_id]
            return payload

        return payload


class TestFCMWebProvider(SimpleTestCase):
    @patch('notifications.providers.FCMWebNotificationProvider.HAS_DEPENDENCIES', False)
    def test_fcm_web_dependency(self):
        fcm_web_notification_channel = FCMWebNotificationChannel({})

        with self.assertRaises(ImproperlyConfiguredProvider):
            fcm_web_notification_channel.notify()

    @patch('notifications.default_settings.NOTIFICATIONS_FCM_WEB_API_KEY', 'api_key')
    @patch('notifications.providers.fcm_web.FCMNotification.notify_single_device')
    def test_fcm_web(self, mocked_notify_single_device):
        mocked_notify_single_device.return_value = {'failure': 0}

        fcm_web_notification_channel = FCMWebNotificationChannel({})
        fcm_web_notification_channel.notify()
        mocked_notify_single_device.assert_called_with(
            registration_id='12345', message_title='Hello', message_body='Hello world'
        )

    @patch('notifications.default_settings.NOTIFICATIONS_FCM_WEB_API_KEY', 'api_key')
    @patch('notifications.providers.fcm_web.FCMNotification.notify_multiple_devices')
    def test_fcm_web_bulk(self, mocked_notify_multiple_devices):
        mocked_notify_multiple_devices.return_value = {'failure': 0}

        fcm_web_notification_channel = FCMWebNotificationChannel(
            {}, context={'bulk': True}
        )
        fcm_web_notification_channel.notify()
        mocked_notify_multiple_devices.assert_called_with(
            message_title='Hello',
            message_body='Hello world',
            registration_ids=['12345'],
        )

    @patch('notifications.default_settings.NOTIFICATIONS_FCM_WEB_API_KEY', 'api_key')
    @patch('notifications.providers.fcm_web.FCMNotification.notify_single_device')
    def test_fcm_web_failed(self, mocked_notify_single_device):
        mocked_notify_single_device.return_value = {'failure': 1}

        fcm_web_provider = FCMWebNotificationProvider()
        mocked_error_logger = Mock()
        fcm_web_provider.logger.error = mocked_error_logger

        fcm_web_provider.send(
            dict(
                message_title='Hello',
                message_body='Hello world',
                registration_id='12345',
            )
        )
        mocked_notify_single_device.assert_called_with(
            registration_id='12345', message_title='Hello', message_body='Hello world'
        )
        mocked_error_logger.assert_called_once()
        mocked_error_logger.assert_called_with({'failure': 1})

    @patch('notifications.default_settings.NOTIFICATIONS_FCM_WEB_API_KEY', 'api_key')
    @patch('notifications.providers.fcm_web.FCMNotification.notify_multiple_devices')
    def test_fcm_web_bulk_failed(self, mocked_notify_multiple_devices):
        mocked_notify_multiple_devices.return_value = {'failure': 2}

        fcm_web_provider = FCMWebNotificationProvider()
        mocked_error_logger = Mock()
        fcm_web_provider.logger.error = mocked_error_logger

        fcm_web_provider.send_bulk(
            dict(
                message_title='Hello',
                message_body='Hello world',
                registration_ids=['12345'],
            )
        )
        mocked_notify_multiple_devices.assert_called_with(
            registration_ids=['12345'],
            message_title='Hello',
            message_body='Hello world',
        )
        mocked_error_logger.assert_called_once()
        mocked_error_logger.assert_called_with({'failure': 2})

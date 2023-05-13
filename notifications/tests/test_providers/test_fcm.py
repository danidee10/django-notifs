from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from notifications.channels import BaseNotificationChannel
from notifications.exceptions import ImproperlyConfiguredProvider
from notifications.providers import FCMNotificationProvider


class FCMNotificationChannel(BaseNotificationChannel):
    name = 'fcm_notification_channel'
    providers = ['fcm']

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


class TestFCMProvider(SimpleTestCase):
    @patch('notifications.providers.FCMNotificationProvider.HAS_DEPENDENCIES', False)
    def test_fcm_dependency(self):
        fcm_notification_channel = FCMNotificationChannel({})

        with self.assertRaises(ImproperlyConfiguredProvider):
            fcm_notification_channel.notify()

    @patch('notifications.default_settings.NOTIFICATIONS_FCM_API_KEY', 'api_key')
    @patch('pyfcm.FCMNotification.notify_single_device')
    def test_fcm(self, mocked_notify_single_device):
        mocked_notify_single_device.return_value = {'failure': 0}

        fcm_notification_channel = FCMNotificationChannel({})
        fcm_notification_channel.notify()
        mocked_notify_single_device.assert_called_with(
            registration_id='12345', message_title='Hello', message_body='Hello world'
        )

    @patch('notifications.default_settings.NOTIFICATIONS_FCM_API_KEY', 'api_key')
    @patch('pyfcm.FCMNotification.notify_multiple_devices')
    def test_fcm_bulk(self, mocked_notify_multiple_devices):
        mocked_notify_multiple_devices.return_value = {'failure': 0}

        fcm_notification_channel = FCMNotificationChannel(
            {}, context={'bulk': True}
        )
        fcm_notification_channel.notify()
        mocked_notify_multiple_devices.assert_called_with(
            message_title='Hello',
            message_body='Hello world',
            registration_ids=['12345'],
        )

    @patch('notifications.default_settings.NOTIFICATIONS_FCM_API_KEY', 'api_key')
    @patch('pyfcm.FCMNotification.notify_single_device')
    def test_fcm_failed(self, mocked_notify_single_device):
        mocked_notify_single_device.return_value = {'failure': 1}

        fcm_provider = FCMNotificationProvider()
        mocked_error_logger = Mock()
        fcm_provider.logger.error = mocked_error_logger

        fcm_provider.send(
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

    @patch('notifications.default_settings.NOTIFICATIONS_FCM_API_KEY', 'api_key')
    @patch('pyfcm.FCMNotification.notify_multiple_devices')
    def test_fcm_bulk_failed(self, mocked_notify_multiple_devices):
        mocked_notify_multiple_devices.return_value = {'failure': 2}

        fcm_provider = FCMNotificationProvider()
        mocked_error_logger = Mock()
        fcm_provider.logger.error = mocked_error_logger

        fcm_provider.send_bulk(
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

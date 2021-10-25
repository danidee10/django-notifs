from django.conf import settings
from django.test import TestCase, override_settings
from django.utils.module_loading import import_string

from notifications.channels import BaseNotificationChannel


class TestNotification(BaseNotificationChannel):
    name = 'test_notification'
    providers = ['email', 'slack', 'django_sms', 'twitter_status_update']

    message = 'Hello world'

    def build_payload(self, provider):
        if provider == 'email':
            return dict(
                subject="Welcome",
                body=self.message,
                to=["Daniel <osaetindaniel@gmail.com>"],
                tags=["Onboarding"],
            )

        if provider == 'slack':
            return {
                'channel': '#general',
                'text': self.message,
            }

        if provider == 'django_sms':
            return {
                'body': self.message,
                'originator': '+15075788089',
                'recipients': ['+1348160307160'],
            }

        if provider == 'twitter_status_update':
            return {
                'status': '.',
                'in_reply_to_status_id': '1234567890',
            }

    def get_delivery_backend(self):
        return import_string(settings.NOTIFICATIONS_DELIVERY_BACKEND)


@override_settings(NOTIFICATIONS_DELIVERY_BACKEND='notifications.backends.Console')
class TestNotificationProviders(TestCase):
    """Test providers with the Console Backend"""

    def test_providers(self):
        test_notification = TestNotification({}, context={})
        test_notification.notify()

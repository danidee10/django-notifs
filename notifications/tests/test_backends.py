"""General Tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from ..backends import RQ, Celery, Channels
from ..channels import ConsoleNotificationChannel
from ..consumers import DjangoNotifsConsumer
from ..tasks import consume
from ..utils import get_notification_model

Notification = get_notification_model()


class BackendTests(TestCase):
    """
    Tests for the Delivery backends

    This class also contains tests for asynchronous functions/methods
    that aren't triggered from the regular unit tests
    """

    User = get_user_model()

    @classmethod
    def setUpTestData(cls):
        """Create Users."""
        cls.user1 = cls.User.objects.create_user(
            username='user1@gmail.com', password='password'
        )

        cls.user2 = cls.User.objects.create_user(
            username='user2@gmail.com', password='password'
        )

        cls.notification = Notification(
            source=cls.user2,
            source_display_name='User 2',
            recipient=cls.user1,
            action='Notified',
            category='General notification',
            obj=cls.user2,
            url='http://example.com',
            short_description='Short Description',
            is_read=False,
        )

    @override_settings(CELERY_BROKER_URL='redis://localhost:6379/0')
    def test_celery_backend(self):
        delivery_backend = Celery(ConsoleNotificationChannel(self.notification))

        self.assertIsNone(delivery_backend.run(countdown=0))

    @override_settings(
        CHANNEL_LAYERS={
            'django_notifs': {
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                    "hosts": [('127.0.0.1', 6379)],
                },
            },
        }
    )
    def test_channels_backend(self):
        delivery_backend = Channels(ConsoleNotificationChannel(self.notification))

        self.assertIsNone(delivery_backend.run(countdown=0))

    def test_rq_backend(self):
        delivery_backend = RQ(ConsoleNotificationChannel(self.notification))

        self.assertIsNone(delivery_backend.run(countdown=0))

    def test_celery_task(self):
        """This ensures that the Celery task runs without errors."""
        self.assertIsNone(
            consume(
                'console',
                'notifications.providers.ConsoleNotificationProvider',
                self.notification.to_json(),
                dict(),
            )
        )

    async def test_channels_consumer(self):
        """This ensures that the Channels consumer runs without errors."""
        consumer = DjangoNotifsConsumer()
        message = {
            'provider': 'console',
            'provider_class': 'notifications.providers.ConsoleNotificationProvider',
            'payload': self.notification.to_json(),
            'context': {},
            'countdown': 0,
        }
        result = await consumer.notify(message)
        self.assertIsNone(result)

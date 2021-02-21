"""General Tests."""

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Notification
from ..tasks import send_notification
from ..backends import Celery, Channels, RQ
from ..consumers import DjangoNotifsConsumer


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

        cls.user2 = cls.User.objects.create(
            username='user2@gmail.com', password='password'
        )

        cls.notification = Notification(
            source=cls.user2, source_display_name='User 2',
            recipient=cls.user1, action='Notified',
            category='General notification', obj=1, url='http://example.com',
            short_description='Short Description', is_read=False,
        )

    def test_celery_backend(self):
        delivery_backend = Celery(self.notification)

        self.assertIsNone(delivery_backend.run())

    def test_channels_backend(self):
        delivery_backend = Channels(self.notification)

        self.assertIsNone(delivery_backend.run())

    def test_rq_backend(self):
        delivery_backend = RQ(self.notification)

        self.assertIsNone(delivery_backend.run())

    def test_celery_task(self):
        """This ensures that the Celery task runs without errors."""
        self.assertIsNone(
            send_notification(self.notification.to_json(), 'console')
        )

    def test_channels_consumer(self):
        """This ensures that the Channels consumer runs without errors."""
        consumer = DjangoNotifsConsumer()
        message = {
            'notification': self.notification.to_json(),
            'channel_alias': 'console'
        }
        self.assertIsNone(consumer.notify(message))

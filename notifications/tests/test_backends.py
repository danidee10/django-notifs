"""
Backend tests.

These tests are neccessary because the general tests
don't test the `run` function of the asynchronous backends.
They simply deliver/enqueue the task.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Notification
from ..backends.rq import RQBackend
from ..backends.celery import CeleryBackend


class BackendTestCase(TestCase):
    """Tests for the asynchronous backends"""

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

    def test_celery_backend(self):
        """
        test the `run` method of the celery backend class

        There's really nothing to assert here but `send_notification`
        should run without any Exception.
        (This might change in the future)
        """
        notification = Notification(
            source=self.user2, source_display_name='User 2',
            recipient=self.user1, action='Notified',
            category='Silent notification', obj=1, url='http://example.com',
            short_description='Short Description', is_read=False,
            channels=('console',)
        )

        self.assertIsNone(CeleryBackend(notification).run())

    def test_rq_backend(self):
        """test the `run` method of the rq backend class"""
        notification = Notification(
            source=self.user2, source_display_name='User 2',
            recipient=self.user1, action='Notified',
            category='Silent notification', obj=1, url='http://example.com',
            short_description='Short Description', is_read=False,
            channels=('console',)
        )

        self.assertIsNone(RQBackend(notification).run())

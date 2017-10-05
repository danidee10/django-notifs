from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Notification
from .signals import read
from . import NotificationError


User = get_user_model()


class NotificationSignalTestCase(TestCase):
    """Tests for the notifications app."""

    @classmethod
    def setUpTestData(cls):
        """Create Users."""
        cls.user1 = User.objects.create_user(
            username='user1@gmail.com', password='password'
            )

        cls.user2 = User.objects.create(
            username='user2@gmail.com', password='password'
            )

    def test_user_cant_read_others_notifications(self):
        """A user should only be able to read THEIR notifications."""
        # Create NOtification for User2
        notification = Notification.objects.create(
            source=self.user1, source_display_name='User 1',
            recipient=self.user2, action='Notified',
            category='General notification', obj=1, url='http://example.com',
            is_read=False
        )

        # Try and Read the notification as User1
        self.assertRaises(
            NotificationError,

            read.send,
            sender=self.__class__, notify_id=notification.id,
            recipient=self.user1
            )

    def test_user_can_read_notifications(self):
        """A user can read their notification"""
        # Create NOtification for User1
        notification = Notification.objects.create(
            source=self.user2, source_display_name='User 2',
            recipient=self.user1, action='Notified',
            category='General notification', obj=1, url='http://example.com',
            is_read=False
        )

        # Try and Read the notification as user1
        read.send(
            sender=self.__class__, notify_id=notification.id,
            recipient=self.user1
            )

        notification.refresh_from_db()
        self.assertEqual(notification.is_read, True)

"""Tests."""

from django.test import TestCase
from django.contrib.auth import get_user_model

from .signals import read
from . import NotificationError
from .models import Notification


class NotificationSignalTestCase(TestCase):
    """Tests for the notifications app."""

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

    def test_to_json(self):
        """Test JSON Representation."""
        # Create notification
        notification = Notification.objects.create(
            source=self.user2, source_display_name='User 2',
            recipient=self.user1, action='Notified',
            category='General notification', obj=1, url='http://example.com',
            short_description='Short Description', is_read=False
        )

        self.assertEqual(
            notification.to_json(),
            {
                'source': 'user2@gmail.com', 'source_display_name': 'User 2',
                'recipient': 'user1@gmail.com', 'action': 'Notified',
                'category': 'General notification', 'obj': 1,
                'short_description': 'Short Description',
                'url': 'http://example.com', 'is_read': False
            }
        )
"""General Tests."""

import time
from unittest import mock

from django.db import models
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from ..utils import notify, read, get_notification_model
from .. import NotificationError
from ..models import BaseNotificationModel
from ..backends.base import BaseBackend
from ..channels import ConsoleNotificationChannel


Notification = get_notification_model()


class NotificationTestCase(TestCase):
    """Tests for the notifications"""

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

    def test_consume(self):
        """
        This is the default method that's used by all backends

         There's really nothing to assert here but `consume`
         should run without any Exception.
         (This might change in the future)
        """
        notification = Notification(
            source=self.user2,
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            category='Silent notification',
            obj=self.user2,
            url='http://example.com',
            short_description='Short Description',
            is_read=False,
            channels=('console',),
        )

        self.assertIsNone(
            BaseBackend.consume(
                'console',
                'notifications.providers.ConsoleNotificationProvider',
                notification.to_json(),
                dict(),
            )
        )

    def test_user_cant_read_others_notifications(self):
        """A user should only be able to read THEIR notifications."""
        # Create Notification for User2
        notification = Notification.objects.create(
            source=self.user1,
            source_display_name='User 1',
            recipient=self.user2,
            action='Notified',
            category='General notification',
            obj=self.user2,
            url='http://example.com',
            is_read=False,
        )

        # Try and Read the notification as User1
        self.assertRaises(
            NotificationError,
            read,
            notify_id=notification.id,
            recipient=self.user1,
        )

    def test_user_can_read_notifications(self):
        """A user can read their notification"""
        # Create Notification for User1
        notification = Notification.objects.create(
            source=self.user2,
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            category='General notification',
            obj=self.user2,
            url='http://example.com',
            is_read=False,
        )

        # Try and Read the notification as user1
        read(notify_id=notification.id, recipient=self.user1)

        notification.refresh_from_db()
        self.assertEqual(notification.is_read, True)

    def test_silent_notification(self):
        """Test Silent notifications."""
        notify(
            source=self.user2,
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            category='Silent notification',
            obj=self.user2,
            url='http://example.com',
            short_description='Short Description',
            is_read=False,
            silent=True,
            channels=('console',),
        )

        notifications = Notification.objects.all()

        self.assertEqual(notifications.count(), 0)

    @mock.patch('notifications.providers.ConsoleNotificationProvider.send_bulk')
    def test_bulk_notification_notify(self, send_bulk):
        notify(
            source=self.user2,
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            category='Silent notification',
            obj=self.user2,
            url='http://example.com',
            short_description='Short Description',
            is_read=False,
            channels=('console',),
            extra_data={
                'context': {
                    'bulk': True,
                }
            },
        )

        send_bulk.assert_called_once_with(
            {'context': {'bulk': True}, 'payload': 'console'}
        )

    @mock.patch('notifications.providers.ConsoleNotificationProvider.send_bulk')
    def test_bulk_notification_direct(self, send_bulk):
        notification = Notification.objects.create(
            source=self.user2,
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            category='Silent notification',
            obj=self.user2,
            url='http://example.com',
            short_description='Short Description',
            is_read=False,
        )
        console_notification = ConsoleNotificationChannel(
            notification, context={'bulk': True}
        )
        payload = console_notification.build_payload('console')
        console_notification.notify()

        send_bulk.assert_called_once_with(payload)

    def test_notify_invalid_channel(self):
        """An invalid channel should raise a AttributeError."""
        notification_kwargs = dict(
            source=self.user2,
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            category='Silent notification',
            obj=self.user2,
            url='http://example.com',
            short_description='Short Description',
            is_read=False,
            channels=('invalid channel',),
        )

        self.assertRaises(AttributeError, notify, **notification_kwargs)

    def test_send_invalid_provider(self):
        """An invalid provider_path should raise an AttributeError."""
        notification = Notification(
            source=self.user2,
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            category='Silent notification',
            obj=self.user2,
            url='http://example.com',
            short_description='Short Description',
            is_read=False,
            channels=('invalid channel',),
        )

        self.assertRaises(
            ImportError,
            BaseBackend.consume,
            'console',
            'notifications.providers.InvalidNotificationProvider',
            notification.to_json(),
            dict(),
        )

    def test_queryset_methods(self):
        """Test the custom queryset methods."""
        for count in range(3):
            Notification.objects.create(
                source=self.user2,
                source_display_name='User 2',
                recipient=self.user1,
                action='Notified ' + str(count),
                category='General notification',
                obj=self.user2,
                url='http://example.com',
                is_read=False,
            )

        notification = Notification.objects.create(
            source=self.user2,
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            category='General notification',
            obj=self.user2,
            url='http://example.com',
            is_read=False,
        )
        read(notify_id=notification.id, recipient=self.user1)

        self.assertEqual(Notification.objects.all_unread().count(), 3)
        self.assertEqual(Notification.objects.all_read().count(), 1)

    def test_string_representation(self):
        """Test the string representation of the Notification model."""
        notification = Notification.objects.create(
            source=self.user2,
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            category='Admin notification',
            obj=self.user2,
            url='http://example.com',
            is_read=False,
        )
        self.assertEqual(
            str(notification),
            'Admin notification: user2@gmail.com Notified  => user1@gmail.com',
        )

        notification = Notification.objects.create(
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            short_description='Admin was  notified',
            category='Admin notification',
            obj=self.user2,
            url='http://example.com',
            is_read=False,
        )
        self.assertEqual(str(notification), 'Admin was  notified')

    def test_notify_countdown(self):
        """
        The notification should only be sent after

        the specified countdown.
        """
        start_time = time.time()
        notify(
            source=self.user2,
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            category='Silent notification',
            obj=self.user2,
            url='http://example.com',
            short_description='Short Description',
            is_read=False,
            channels=('console',),
            countdown=3,
        )
        total_time = time.time() - start_time

        self.assertGreater(total_time, 3)


class CustomNotificationModel(BaseNotificationModel):
    class Meta:
        db_table = 'notifications_notification'
        managed = False

    recipient = models.ForeignKey(
        get_user_model(),
        related_name='custom_notifs_notifications',
        null=True,
        on_delete=models.CASCADE,
    )

    def to_json(self):
        return 'custom notification model'


@override_settings(
    NOTIFICATIONS_MODEL='notifications.tests.test_general.CustomNotificationModel'
)
class CustomNotificationTestCase(TestCase):
    """Tests for the custom Notification model functionality"""

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

    def test_import_custom_notification_model(self):
        """The NOTIFICATIONS_MODEL setting should be applied."""
        Notification = get_notification_model()
        notification = Notification(
            source=self.user2,
            source_display_name='User 2',
            recipient=self.user1,
            action='Notified',
            category='Silent notification',
            obj=self.user2,
            url='http://example.com',
            short_description='Short Description',
            is_read=False,
            channels=('console',),
        )

        self.assertEqual(notification.to_json(), 'custom notification model')

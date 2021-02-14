"""Adpaters to send notifications through various meduiums."""

from django.conf import settings

from .base import BaseNotificationChannel

import requests


class PushNotificationChannel(BaseNotificationChannel):
    """Push notification channel."""

    def notify(self, message):
        """Send the notification."""
        kwargs = self.notification_kwargs
        # message = self.construct_message()

        # Send push notification(s)
        subject = '{} {} {}'.format(
            kwargs['source_display_name'], kwargs['action'],
            kwargs.get('short_description', '')
        )
        icon = kwargs.get('icon')
        token = kwargs.get('extra_data', {}).get('token', '')

        if token:
            requests.post(
                'https://fcm.googleapis.com/fcm/send',
                json={
                    'notification': {
                        'title': subject,
                        # 'body': message,
                        'click_action': kwargs.get('url', ''),
                        'icon': icon
                    },
                    'to': token
                },
                headers={'Authorization': 'key=' + settings.FCM_KEY}
            )

"""Adpaters to send notifications through various meduiums."""

from django.conf import settings

from . import BaseNotificationProvider

import requests


class PushNotificationProvider(BaseNotificationProvider):
    """Google FCM Provider."""

    name = 'push_notification_fcm'

    def send(self, payload):
        requests.post(
            'https://fcm.googleapis.com/fcm/send',
            json={
                'notification': {
                    'title': payload['subject'],
                    'body': payload['body'],
                    'click_action': payload['url'],
                    'icon': payload['icon'],
                },
                'to': payload['token'],
            },
            headers={'Authorization': 'key={}'.format(settings.NOTIFICATIONS_FCM_KEY)},
        )

    def send_bulk(self, payloads):
        for payload in payloads:
            self.send(payload)

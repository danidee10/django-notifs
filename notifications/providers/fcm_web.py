"""Adpaters to send notifications through various meduiums."""

import requests
from django.conf import settings

from . import BaseNotificationProvider


class FCMWebNotificationProvider(BaseNotificationProvider):
    """Google FCM Web Provider."""

    name = 'fcm_web'

    def send(self, payload):
        requests.post(
            'https://fcm.googleapis.com/fcm/send',
            json={
                'notification': {
                    'title': payload['title'],
                    'body': payload['body'],
                    'click_action': payload['click_action'],
                    'icon': payload['icon'],
                },
                'to': payload['to'],
            },
            headers={
                'Authorization': 'key={}'.format(settings.NOTIFICATIONS_FCM_WEB_KEY)
            },
        )

    def send_bulk(self, payloads):
        for payload in payloads:
            self.send(payload)

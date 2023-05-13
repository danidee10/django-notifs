"""Deprecated FCM Adapter. Use the new 'fcm' backend"""

from typing import Dict

from pydantic import BaseModel, conlist

from notifications import default_settings as settings

from . import BaseNotificationProvider


class BaseFCMSchema(BaseModel):
    pass


class FCMWebSchema(BaseFCMSchema):
    pass


class BulkFCMWebSchema(BaseFCMSchema):
    registration_ids: conlist(Dict, min_items=1)


import requests
from django.conf import settings

from . import BaseNotificationProvider


class FCMWebNotificationProvider(BaseNotificationProvider):
    """Google FCM Web Provider."""

    name = 'fcm_web'
    HAS_DEPENDENCIES = True

    def get_validator(self):
        if self.context.get('bulk', False) is True:
            return BulkFCMWebSchema

        return FCMWebSchema

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

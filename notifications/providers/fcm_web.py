from typing import Dict, Optional

from pydantic import BaseModel, conlist

try:
    from pyfcm import FCMNotification

    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False

from notifications import default_settings as settings

from . import BaseNotificationProvider


class BaseFCMSchema(BaseModel):
    message_title: Optional[str]
    message_body: Optional[str]
    message_icon: Optional[str]
    sound: str = 'default'
    data_message: Optional[Dict]


class FCMWebSchema(BaseFCMSchema):
    registration_id: str


class BulkFCMWebSchema(BaseFCMSchema):
    registration_ids: conlist(str, min_items=1)


class FCMWebNotificationProvider(BaseNotificationProvider):
    """Google FCM Web Provider."""

    name = 'fcm_web'
    package = 'pyfcm'

    HAS_DEPENDENCIES = HAS_DEPENDENCIES

    def __init__(self, context=dict()):
        super().__init__(context=context)
        self.fcm_client = FCMNotification(
            api_key=settings.NOTIFICATIONS_FCM_WEB_API_KEY,
            proxy_dict=settings.NOTIFICATIONS_FCM_WEB_PROXY,
        )

    def get_validator(self):
        if self.context.get('bulk', False) is True:
            return BulkFCMWebSchema

        return FCMWebSchema

    def send(self, payload):
        response = self.fcm_client.notify_single_device(**payload)
        if response['failure'] != 0:
            self.logger.error(response)

        return response

    def send_bulk(self, payloads):
        response = self.fcm_client.notify_multiple_devices(**payloads)
        if response['failure'] != 0:
            self.logger.error(response)

        return response

"""Celery backend"""

from __future__ import absolute_import, unicode_literals


from celery import shared_task
from celery.utils.log import get_task_logger

from .base import BaseBackend
from .utils import _send_notification
from .. import default_settings as settings


logger = get_task_logger(__name__)

autoretry_for = []
if settings.NOTIFICATIONS_RETRY:
    autoretry_for.append(Exception)


@shared_task(
    autoretry_for=autoretry_for,
    retry_backoff=settings.NOTIFICATIONS_RETRY_INTERVAL,
    max_retries=settings.NOTIFICATIONS_MAX_RETRIES
)
def send_notification(notification, channel_alias):
    """Send notification via a channel to celery."""
    _send_notification(notification, channel_alias, logger)


class CeleryBackend(BaseBackend):
    def run(self):
        for channel_alias in self.notification["channels"]:
            send_notification.apply_async(
                args=[self.notification, channel_alias],
                queue=settings.NOTIFICATIONS_QUEUE_NAME,
            )

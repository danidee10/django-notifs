"""Celery backend"""

from __future__ import absolute_import, unicode_literals

from .. import default_settings as settings

from celery import shared_task
from celery.utils.log import get_task_logger

from .base import BaseBackend
from .utils import _send_notification


logger = get_task_logger(__name__)


@shared_task
def send_notification(notification):
    """Send notification via a channel to celery."""
    _send_notification(notification, logger)


class CeleryBackend(BaseBackend):

    def run(self):
        send_notification.apply_async(
            args=[self.notification.to_json()],
            queue=settings.NOTIFICATIONS_QUEUE_NAME
        )

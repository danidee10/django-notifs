"""Celery backend"""

from __future__ import absolute_import, unicode_literals

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
        send_notification.delay(self.notification.to_json())

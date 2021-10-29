"""Celery backend"""

from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from .. import default_settings as settings
from .base import BaseBackend

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    retry_backoff=settings.NOTIFICATIONS_RETRY_INTERVAL,
    max_retries=settings.NOTIFICATIONS_MAX_RETRIES,
)
def consume(self, provider, payload, context):
    """Send notification via a channel to celery."""
    try:
        CeleryBackend.consume(provider, payload, context)
    except Exception as e:
        if settings.NOTIFICATIONS_RETRY:
            self.retry(exc=e)


class CeleryBackend(BaseBackend):
    def produce(self, provider, payload, context, countdown):
        consume.apply_async(
            args=[provider, payload, context],
            queue=settings.NOTIFICATIONS_QUEUE_NAME,
            countdown=countdown,
        )

"""Celery backend"""

from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from .. import default_settings as settings
from .base import BaseBackend

logger = get_task_logger(__name__)

autoretry_for = []
if settings.NOTIFICATIONS_RETRY:
    autoretry_for.append(Exception)


@shared_task(
    autoretry_for=autoretry_for,
    retry_backoff=settings.NOTIFICATIONS_RETRY_INTERVAL,
    max_retries=settings.NOTIFICATIONS_MAX_RETRIES,
)
def consume(alias, provider_class, payload, context):
    """Send notification via a channel to celery."""
    CeleryBackend.consume(alias, provider_class, payload, context)


class CeleryBackend(BaseBackend):
    def produce(self, provider, provider_class, payload, context, countdown):
        consume.apply_async(
            args=[provider, provider_class, payload, context],
            queue=settings.NOTIFICATIONS_QUEUE_NAME,
            countdown=countdown,
        )

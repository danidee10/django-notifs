"""RQ Backend"""

import logging
from datetime import timedelta

import django_rq
from rq import Retry

from .. import default_settings as settings
from .base import BaseBackend

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('django_notifs.backends.rq')

retry = None
if settings.NOTIFICATIONS_RETRY:
    retry = Retry(
        max=settings.NOTIFICATIONS_MAX_RETRIES,
        interval=settings.NOTIFICATIONS_RETRY_INTERVAL,
    )


class RQBackend(BaseBackend):
    def produce(self, provider, provider_class, payload, context, countdown):
        queue = django_rq.get_queue(settings.NOTIFICATIONS_QUEUE_NAME)
        queue.enqueue_in(
            timedelta(seconds=countdown),
            self.consume,
            provider,
            provider_class,
            payload,
            context,
            retry=retry,
        )

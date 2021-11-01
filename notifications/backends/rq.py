"""RQ Backend"""

import logging
from datetime import timedelta

import django_rq
from rq import Retry

from .. import default_settings as settings
from .base import BaseBackend


class RQBackend(BaseBackend):

    logger = logging.getLogger('django_notifs.backends.base')

    def produce(self, provider, payload, context, countdown):
        retry = None
        if settings.NOTIFICATIONS_RETRY:
            retry = Retry(
                max=settings.NOTIFICATIONS_MAX_RETRIES,
                interval=settings.NOTIFICATIONS_RETRY_INTERVAL,
            )

        queue = django_rq.get_queue(settings.NOTIFICATIONS_QUEUE_NAME)
        queue.enqueue_in(
            timedelta(seconds=countdown),
            self.consume,
            provider,
            payload,
            context,
            retry=retry,
        )

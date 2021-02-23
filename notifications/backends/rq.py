"""RQ Backend"""

import logging

import django_rq
from rq import Retry

from .base import BaseBackend
from .utils import _send_notification
from .. import default_settings as settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('django_notifs.backends.rq')

retry = None
if settings.NOTIFICATIONS_RETRY:
    retry = Retry(
        max=settings.NOTIFICATIONS_MAX_RETRIES,
        interval=settings.NOTIFICATIONS_RETRY_INTERVAL
    )


class RQBackend(BaseBackend):

    def run(self):
        for channel_alias in self.notification['channels']:
            queue = django_rq.get_queue(settings.NOTIFICATIONS_QUEUE_NAME)
            queue.enqueue(
                _send_notification, self.notification, channel_alias, logger,
                retry=retry
            )

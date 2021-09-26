"""Synchronous backend"""

import logging
import time

from .base import BaseBackend


class SynchronousBackend(BaseBackend):
    logger = logging.getLogger('django_notifs.backends.synchronous')

    def deliver(self, provider, provider_class, payload, context, countdown):
        time.sleep(countdown)
        self.send_notification(provider, provider_class, payload, context)

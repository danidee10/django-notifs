"""Synchronous backend"""

import logging
import time

from .base import BaseBackend


class SynchronousBackend(BaseBackend):
    logger = logging.getLogger('django_notifs.backends.synchronous')

    def produce(self, provider, provider_class, payload, context, countdown):
        time.sleep(countdown)
        self.consume(provider, provider_class, payload, context)

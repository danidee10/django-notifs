"""Synchronous backend"""

import time
import logging

from .base import BaseBackend
from .utils import _send_notification


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('django_notifs.backends.synchronous')


class SynchronousBackend(BaseBackend):

    def run(self, countdown):
        for channel_alias in self.notification['channels']:
            time.sleep(countdown)
            _send_notification(self.notification, channel_alias, logger)

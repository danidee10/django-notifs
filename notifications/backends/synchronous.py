"""Synchronous backend"""

import logging

from .base import BaseBackend
from .utils import _send_notification


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('django_notifs.backends.synchronous')


class SynchronousBackend(BaseBackend):

    def run(self):
        for channel_alias in self.notification['channels']:
            _send_notification(self.notification, channel_alias, logger)

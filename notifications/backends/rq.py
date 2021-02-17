"""RQ Backend"""

import logging

import django_rq

from .base import BaseBackend
from .utils import _send_notification


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('django_notifs.backends.rq')


class RQBackend(BaseBackend):

    def run(self):
        django_rq.enqueue(
            _send_notification, self.notification.to_json(), logger
        )

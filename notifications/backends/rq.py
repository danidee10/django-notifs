"""RQ Backend"""

import logging

from .. import default_settings as settings

import django_rq

from .base import BaseBackend
from .utils import _send_notification


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('django_notifs.backends.rq')


class RQBackend(BaseBackend):

    def run(self):
        queue = django_rq.get_queue(settings.NOTIFICATIONS_QUEUE_NAME)
        queue.enqueue(_send_notification, self.notification.to_json(), logger)

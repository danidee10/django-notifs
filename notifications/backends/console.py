"""Console backend"""

import logging
import time
from unittest.mock import patch

from notifications.providers import BaseNotificationProvider

from .base import BaseBackend


class ConsoleBackend(BaseBackend):
    logger = logging.getLogger('django_notifs.backends.console')

    def produce(self, provider, payload, context, countdown):
        time.sleep(countdown)

        provider_class = BaseNotificationProvider.get_provider_class(provider)
        patcher_send = patch(f'{provider_class}.send')
        patcher_send_bulk = patch(f'{provider_class}.send_bulk')

        patcher_send.start()
        patcher_send_bulk.start()
        self.consume(provider, payload, context)
        patcher_send.stop()
        patcher_send_bulk.stop()

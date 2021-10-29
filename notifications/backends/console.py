"""Console backend"""

import logging
from unittest.mock import patch

from notifications.providers import BaseNotificationProvider

from .synchronous import SynchronousBackend


class ConsoleBackend(SynchronousBackend):
    logger = logging.getLogger('django_notifs.backends.console')

    def produce(self, provider, payload, context, countdown):
        provider_class = BaseNotificationProvider.get_provider_class(provider)
        patcher_send = patch(f'{provider_class}.send')
        patcher_send_bulk = patch(f'{provider_class}.send_bulk')
        patcher_send.start()
        patcher_send_bulk.start()

        super().produce(provider, payload, context, countdown)

        patcher_send.stop()
        patcher_send_bulk.stop()

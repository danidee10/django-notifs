"""Channels consumers."""

import logging

from channels.consumer import SyncConsumer

from notifications.backends.utils import _send_notification


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('django_notifs.backends.channels')


class DjangoNotifsConsumer(SyncConsumer):

    def notify(self, message):
        _send_notification(
            message['notification'], message['channel_alias'], logger
        )

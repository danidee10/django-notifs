"""Channels backend"""

from __future__ import absolute_import, unicode_literals

import channels.layers
from asgiref.sync import async_to_sync

from .. import default_settings as settings

from .base import BaseBackend


class ChannelsBackend(BaseBackend):

    def run(self):
        channel_layer = channels.layers.get_channel_layer(
            settings.NOTIFICATIONS_QUEUE_NAME
        )

        for channel_alias in self.notification['channels']:
            async_to_sync(channel_layer.send)(
                settings.NOTIFICATIONS_QUEUE_NAME,
                {
                    'notification': self.notification,
                    'channel_alias': channel_alias, 'type': 'notify'
                }
            )
"""Channels backend"""

from __future__ import absolute_import, unicode_literals

import channels.layers
from asgiref.sync import async_to_sync

from .. import default_settings as settings
from .base import BaseBackend


class ChannelsBackend(BaseBackend):
    def produce(self, provider, provider_class, payload, context, countdown):
        channel_layer = channels.layers.get_channel_layer(
            settings.NOTIFICATIONS_QUEUE_NAME
        )
        async_to_sync(channel_layer.send)(
            settings.NOTIFICATIONS_QUEUE_NAME,
            {
                'provider': provider,
                'provider_class': provider_class,
                'payload': payload,
                'context': context,
                'countdown': countdown,
                'type': 'notify',
            },
        )

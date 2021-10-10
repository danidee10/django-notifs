"""Base backend."""

import abc
import logging

from django.utils.module_loading import import_string

from notifications.channels import BaseNotificationChannel


class BaseBackend(metaclass=abc.ABCMeta):

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('django_notifs.backends.base')

    def __init__(self, notification_channel: BaseNotificationChannel):
        self.notification_channel = notification_channel

    @staticmethod
    def get_notification_provider(provider_path, context):
        return import_string(provider_path)(context)

    @classmethod
    def consume(cls, provider, provider_class, payload, context):
        notification_channel = cls.get_notification_provider(provider_class, context)

        bulk = context.get('bulk', False)
        if bulk is True:
            notification_channel.send_bulk(payload)
        else:
            notification_channel.send(payload)

        cls.logger.info(
            'Sent notification with the %s provider with context: %s\n'
            % (provider, context)
        )

    @abc.abstractclassmethod
    def produce(self):
        raise NotImplementedError

    def run(self, countdown):
        for (
            provider,
            provider_class,
        ) in self.notification_channel.provider_paths.items():
            payload = self.notification_channel.build_payload(provider)
            context = self.notification_channel.get_context(provider)

            self.produce(provider, provider_class, payload, context, countdown)

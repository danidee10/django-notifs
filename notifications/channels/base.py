import abc

from django.utils.module_loading import import_string

from notifications import default_settings as settings
from notifications.providers import BaseNotificationProvider
from notifications.utils import classproperty


class BaseNotificationChannel(metaclass=abc.ABCMeta):
    def __init__(self, notification, context=dict()):
        self.notification = notification
        self.context = context

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError

    @abc.abstractproperty
    def providers(self):
        return []

    @abc.abstractmethod
    def build_payload(self, provider):
        """Constructs a paylod from the notification object."""
        raise NotImplementedError

    @classproperty
    def registered_channels(cls):
        return {
            klass.name: f'{klass.__module__}.{klass.__name__}'
            for klass in cls.__subclasses__()
        }

    @property
    def provider_paths(self):
        provider_paths = dict()
        for name in self.providers:
            provider_paths[name] = BaseNotificationProvider.get_provider_class(name)

        return provider_paths

    def get_context(self, provider):
        return self.context

    def get_delivery_backend(self):
        return import_string(settings.NOTIFICATIONS_DELIVERY_BACKEND)

    def notify(self, countdown=0):
        delivery_backend = self.get_delivery_backend()
        delivery_backend(self).run(countdown)

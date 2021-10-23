import abc
import importlib

from notifications import InvalidNotificationProvider
from notifications.utils import classproperty


class BaseNotificationProvider(metaclass=abc.ABCMeta):
    def __init__(self, context=dict()):
        self.context = context

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError

    @classproperty
    def providers(cls):
        return {
            klass.name: f'{klass.__module__}.{klass.__name__}'
            for klass in cls.__subclasses__()
        }

    @classmethod
    def get_provider_class(cls, provider):
        try:
            provider_class = cls.providers[provider]
        except KeyError:
            # Generate helpful error if the provider is valid
            # but it's dependencies are missing
            try:
                importlib.import_module(f'notifications.providers.{provider}')
            except ModuleNotFoundError:
                raise InvalidNotificationProvider(
                    f'{provider} is not a valid notification provider.\n'
                    f'Registered providers: {cls.providers}'
                )

        return provider_class

    @abc.abstractmethod
    def send(self, payload):
        raise NotImplementedError

    def send_bulk(self, payloads):
        for payload in payloads:
            self.send(payload)

import abc

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

    @abc.abstractmethod
    def send(self, payload):
        raise NotImplementedError

    def send_bulk(self, payloads):
        for payload in payloads:
            self.send(payload)

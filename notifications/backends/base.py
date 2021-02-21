"""Base backend."""

import abc


class BaseBackend(metaclass=abc.ABCMeta):

    def __init__(self, notification):
        self.notification = notification.to_json()

    @abc.abstractmethod
    def run(self):
        pass

"""Base backend."""

import abc


class BaseBackend(metaclass=abc.ABCMeta):

    def __init__(self, notification):
        self.notification = notification

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

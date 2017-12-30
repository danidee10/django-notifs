"""Base Implementation of a Delivery Backend."""

import abc


class BaseNotificationChannel(metaclass=abc.ABCMeta):
    """Base channel for sending notifications."""

    def __init__(self, **kwargs):
        self.notifcation_kwargs = kwargs

    @abc.abstractmethod
    def construct_message(self):
        """Constructs a message from notification details."""
        pass

    @abc.abstractmethod
    def notify(self):
        """Sends the notification."""
        pass

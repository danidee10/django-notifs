import abc


class BaseNotificationChannel(metaclass=abc.ABCMeta):
    """Base channel for sending notifications."""

    def __init__(self, **kwargs):
        self.notification_kwargs = kwargs

    @abc.abstractmethod
    def construct_message(self):
        """Constructs a message from notification details."""
        raise NotImplementedError

    @abc.abstractmethod
    def notify(self, message):
        """Sends the notification."""
        raise NotImplementedError

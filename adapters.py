"""Adapters to send notification with different mediums."""
import abc

class BaseAdapter(metaclass=abc.ABCMeta):
    """Base adapter for sending notifications."""

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @abc.abstractmethod
    def construct_message(self):
        """Constructs a message from notification details."""
        pass

    @abc.abstractmethod
    def notify(self):
        """Sends the notification."""
        pass

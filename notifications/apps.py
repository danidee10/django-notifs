"""Register all Signals."""

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """App Config."""
    
    name = 'notifications'

    def ready(self):
        """Import signals."""
        from . import signals

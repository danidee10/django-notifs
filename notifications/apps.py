"""Register all Signals."""

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """App Config."""

    name = 'notifications'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        """Import signals."""
        from . import signals

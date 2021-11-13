"Notifications app config"

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """App Config."""

    name = 'notifications'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        # override settings/set default settings
        # from django.conf import settings
        # from notifications import default_settings

        # for setting in dir(default_settings):
        #    if setting.startswith('NOTIFICATIONS_'):
        #        setattr(settings, setting, getattr(default_settings, setting))

        import notifications.signals  # noqa

from pydantic import ValidationError


class NotificationError(Exception):
    """Custom error type for the app."""

    pass


class ImproperlyInstalledNotificationProvider(ImportError):
    """Exception for missing provider dependencies"""

    def __init__(self, missing_package, provider):
        message = (
            f'The `{missing_package}` package is required to use this Provider, '
            "but it isn't installed.\n"
            f'(Be sure to use `pip install django-notifs[{provider}]`)'
        )
        super().__init__(message)


class InvalidNotificationProvider(Exception):
    pass


class InvalidNotificationProviderPayload(ValidationError):
    pass


default_app_config = 'notifications.apps.NotificationsConfig'

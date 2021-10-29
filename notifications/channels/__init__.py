from .base import BaseNotificationChannel  # noqa

try:
    from .django_channels import DjangoWebSocketChannel  # noqa
except ImportError:
    pass

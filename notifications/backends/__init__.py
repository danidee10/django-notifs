from .rq import RQBackend as RQ  # noqa
from .celery import CeleryBackend as Celery  # noqa
from .django_channels import ChannelsBackend as Channels  # noqa
from .synchronous import SynchronousBackend as Synchronous  # noqa

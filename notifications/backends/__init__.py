# Optional dependencies are wrapped in try/excepts to prevent
# ImportErrors if the user hasn't installed them
# Surely, there's a better way to handle this :/

try:
    from .rq import RQBackend as RQ  # noqa
except ImportError:
    pass
try:
    from .celery import CeleryBackend as Celery  # noqa
except ImportError:
    pass
try:
    from .django_channels import ChannelsBackend as Channels  # noqa
except ImportError:
    pass

from .synchronous import SynchronousBackend as Synchronous  # noqa

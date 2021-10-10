import os

from channels.routing import ChannelNameRouter, ProtocolTypeRouter
from django.core.asgi import get_asgi_application

from notifications import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifs.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'channel': ChannelNameRouter(
            {
                'django_notifs': consumers.DjangoNotifsConsumer.as_asgi(),
            }
        ),
    }
)

Advanced usage
**************

.. _documentation: https://channels.readthedocs.io/en/stable/index.html
.. _channels deployment documentation: https://channels.readthedocs.io/en/stable/deploying.html

Tentative Notifications
--------------------------------

A tentative notification is a conditional notification that should only be sent if a criteria is met.

An example is sending a notification if a user hasn't read a chat message in 30 minutes (as a reminder).

You can acheive this by combining the ``countdown`` functionality with a custom provider::

    # delay notification for 30 minutes
    notify(**kwargs, countdown=1800)

Custom provider::

    from notifications.utils import get_notification_model
    from notifications.providers import BaseNotificationProvider

    class DelayedNotificationChannel(BaseNotificationProvider):

        def send(self, payload):
            notification_id = self.payload['notification_id']

            notification = get_notification_model().objects.get(id=self.notification_id)
            if notification.read:
                return

            # send the notification

In this example, we abort the notification if the notification has been read but you're free
to use any condition/custom logic


WebSockets
---------------------

Unlike other django notification libraries that provide an API for accessing notifications,
django-notifs supports websockets out of the box (thanks to `django-channels`). This makes it easy to send realtime notifications
to your users in reaction to a new server side event.

If you're unfamiliar with django-channels. It's advised to go through the `documentation`_ so you can understand the basics.


Setting up the WebSocket server
-------------------------------

*This section assumes that you've already installed django-channels*

Setup the consumer routing in your ``asgi.py`` file::

    import os

    import django
    from django.core.asgi import get_asgi_application
    from channels.routing import ProtocolTypeRouter, URLRouter

    from notifications import routing as notifications_routing


    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourapp.settings')

    application = ProtocolTypeRouter({
        'http': get_asgi_application(),
        'websocket': URLRouter(notifications_routing.websocket_urlpatterns)
    })


Notification channels
---------------------
A simple WebSocket channel is provided:

- notifications.channels.WebSocketChannel

This channel simply delivers notifications to the ``settings.NOTIFICATIONS_WEBSOCKET_EVENT_NAME`` group.

Add the channel to ``settings.NOTIFICATION_CHANNELS``::

    NOTIFICATION_CHANNELS = {
        'websocket': 'notifications.channels.WebSocketChannel'
    }

Sample usage::

    from notifications import default_settings as notifs_settings
    ...

    notif_args = {
        'source': user,
        'source_display_name': user.get_full_name(),
        'category': 'MESSAGE', 'action': 'Sent',
        'obj': obj.id,
        'short_description': 'You a new message', 'silent': True,
        'extra_data': {
            notifs_settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM: chat_session.uri,
            'message': chat_session_message.to_json()
        }
    }
    notify(**notif_args, channels=['websocket'])

``notifs_settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM`` is a required key. You can also override it in ``settings.py``
and reference it through ``django.conf.settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM``


Running the WebSocket server
----------------------------

``ASGI`` is capable of handling regular HTTP and WebSocket traffic so you don't really need to run a dedicated
WebSocket server but it's still an option.

see the `channels deployment documentation`_ for more information on the best way to deploy your
application.


How to listen to notifications
------------------------------

You listen to notifications by connecting to the WebSocket URL.

The default URL is ``http://localhost:8000/<settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM>``

To connect to a WebSocket room (via JavaScript) for a user ``danidee`` you'll need to connect to::

    var websocket = new WebSocket('ws://localhost:8000/danidee')

You can always change the default route by Importing the ``notifications.consumers.DjangoNotifsWebsocketConsumer``
consumer and declaring another route. If you decide to do that, make sure you use the
``NOTIFICATIONS_WEBSOCKET_URL_PARAM`` setting because the Consumer class relies on it

an example to prefix the URL with ``/chat`` would be::

    from django.urls import path

    from . import default_settings as settings
    from .consumers import DjangoNotifsWebsocketConsumer

    websocket_urlpatterns = [
        path(
            f'chat/<{settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM}>',
            DjangoNotifsWebsocketConsumer.as_asgi()
        )
    ]


Authentication?
---------------

This is out of the scope of django-notifs for now. This might change in the future as django-channels becomes more mature.
Hence, The WebSocket endpoint is unprotected and you'll probably want to roll out your own custom authentication backend
if you don't make use of the standard Authentication backend.


Testing and Debugging
---------------------

django-notifs comes with an inbuilt ``'console'`` provider that just prints out the notification payload::

    class MyNotificationChannel:
        providers = ['console']
        ...

This can be helpful during development where you don't want notifications to be delivered.

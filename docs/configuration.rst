Configuration
*************

Available settings:

**NOTIFICATIONS_PAGINATE_BY (default=15)**

Pagination to use for Django templates

**NOTIFICATIONS_CHANNELS (default={})**

A dictionary of notification channels.

keys: The softname of the notification channel which is used in your code

values:  The path to the notification channel's class.

Example::

    NOTIFICATIONS_CHANNELS = {
        'console': 'notifications.channels.ConsoleChannel'
    }

django-notifs comes with an inbuilt console delivery channel that just prints out the notification arguments


.. warning::
   This websocket settings have been deperecated and will be removed in a future version

**NOTIFICATIONS_USE_WEBSOCKET (default=False)**

Enable the WebSocket channel. Interally, this adds a new channel ``{'websocket': 'notifications.channels.BasicWebSocketChannel'}`` to ``settings.NOTIFICATIONS_CHANNELS``

**NOTIFICATIONS_RABBIT_MQ_URL (default='amqp://guest:guest@localhost:5672')**

The RabbitMQ URI for the WebSocket channel

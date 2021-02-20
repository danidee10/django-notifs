Configuration
*************

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


**NOTIFICATIONS_DELIVERY_BACKEND (default='notifications.backends.Synchronous')**

``django-notifs`` is designed to support different backends for delivering notifications.
By default it uses the ``Synchronous`` backend which delivers notifications synchronously.

.. note::
   The Synchronous backend is not suitable for production because it blocks the request.
   It's more suitable for testing and debugging.
   To deliver notification asynchronously, please see the :doc:`backends section <./backends>`.

**NOTIFICATIONS_QUEUE_NAME (default='django_notifs')**

**This setting is only valid for the Celery, Channels and RQ backend**

This is the queue name for backends that have a "queue" functionality


**NOTIFICATIONS_USE_WEBSOCKET (default=False)**

.. warning::
   This websocket settings have been deperecated and will be removed in a future version

Enable the WebSocket channel. Interally, this adds a new channel ``{'websocket': 'notifications.channels.BasicWebSocketChannel'}`` to ``settings.NOTIFICATIONS_CHANNELS``

**NOTIFICATIONS_RABBIT_MQ_URL (default='amqp://guest:guest@localhost:5672')**

The RabbitMQ URI for the WebSocket channel

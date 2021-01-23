Advanced usage
**************

WebSockets
---------------------

.. warning::
   This functionality has been deperecated and will probably be replaced by
   *django-channels* or *django-socketio*

This is the coolest part of this library, Unlike other django notification libraries that provide a JavaScript API that the client call poll at regular intervals,
django-notifs supports websockets (thanks to `uWSGI`). This means you can send realtime notifications and possibly use it to build a chat application
or something that requires instant notifications etc

To actually deliver notifications, `django-notifs` uses `RabbitMQ` as a message queue to store notifications which are then consumed and sent over the websocket to the client.

To enable the Websocket functionality simply set:

``NOTIFICATIONS_USE_WEBSOCKET = True``

and set the URL to your RabbitMQ Server with:

``NOTIFICATIONS_RABBIT_MQ_URL = 'YOUR RABBIT MQ SERVER'``

This will tell django-notifs to publish messages to the rabbitmq queue.

Under the hood, django-notifs adds a new channel to ``settings.NOTIFICATIONS_CHANNELS`` which contains the logic for delivering the messages to RabbitMQ. If you need more advanced features that RabbitMQ offers like [Pub/Sub](https://www.rabbitmq.com/tutorials/tutorial-one-python.html) or you want to use a different message queue like Redis, all you need to do is write your own delivery channel and add it to `NOTIFICATIONS_CHANNELS`.

**Running the websocket server**

Due to the fact that Django itself doesn't support websockets, The Websocket server has to be started separately from your main application with uwsgi. For example to start the `WebSocket` Server with `gevent` you can do this:

``uwsgi --http :8080 --gevent 100 --module websocket --gevent-monkey-patch --master --processes 4``

There is a sample echo websocket server in the ``examples`` directory.

**How to listen to notifications**

At the backend, A Rabbitmq queue is created for each user based on the username, so when you're connecting to the websocket server you have to pass the username in the websocket url.
For example, you can listen to messages for the username ``danidee`` connect to this url (Assuming the websocket server is running on `localhost` and port `8080`)

``var websocket = new WebSocket('ws://localhost:8080/danidee')``


Testing and Debugging
---------------------

django-notifs comes with an inbuilt console delivery channel that just prints out the notification arguments::


    NOTIFICATIONS_CHANNELS = {
        'console': 'notifications.channels.ConsoleChannel'
    }


This can be helpful during development.

**Synchronous Notifications**

During development, you might need to send notifications synchronously. You can achieve this by setting ``settings.CELERY_TASK_ALWAYS_EAGER`` to ``True``.

Configuration
*************



``NOTIFICATIONS_CHANNELS``
--------------------------

``Default={}``

A dictionary of notification channels.

**Keys:** The softname of the notification channel which is used in your code

**Values:**  The path to the notification channel's class.

Example::

    NOTIFICATIONS_CHANNELS = {
        'console': 'notifications.channels.ConsoleChannel'
    }

django-notifs comes with an inbuilt console delivery channel that just prints out the notification arguments



``NOTIFICATIONS_DELIVERY_BACKEND``
----------------------------------

``Default='notifications.backends.Synchronous``

``django-notifs`` is designed to support different backends for delivering notifications.
By default it uses the ``Synchronous`` backend which delivers notifications synchronously.

.. note::
   The Synchronous backend is not suitable for production because it blocks the request.
   It's more suitable for testing and debugging.
   To deliver notification asynchronously, please see the :doc:`backends section <./backends>`.



``NOTIFICATIONS_QUEUE_NAME``
----------------------------

``Default='django_notifs'``

**This setting is only valid for the Celery, Channels and RQ backend**

This is the queue name for backends that have a "queue" functionality



``NOTIFICATIONS_RETRY``
-----------------------

``Default=False``

Enable the retry functionality.

**The Retry functionality is only valid for the Celery and RQ backends**


``NOTIFICATIONS_RETRY_INTERVAL``
================================

``Default=5``

The retry interval (in seconds) between each retry


``NOTIFICATIONS_MAX_RETRIES``
=============================

``Default=5``

The maximum number of retries for a notification.



``NOTIFICATIONS_WEBSOCKET_EVENT_NAME``
--------------------------------------

``Default='notifs_websocket_message'``

The ``type`` value of the messages that are going to received by the django notifs websocket consumer.
In most cases, you don't need to change this setting.



``NOTIFICATIONS_WEBSOCKET_URL_PARAM``
--------------------------------------

``Default = 'room_name'``

The WebSocket URL param name. This setting **MUST** be used in the ``notify`` method's ``extra_data`` dictionary.
It's also used to construct the WebSocket URL.
See the :ref:`Advanced usage <Notification channels>` section for more information.

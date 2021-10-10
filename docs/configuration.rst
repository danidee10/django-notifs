Configuration
*************


``NOTIFICATIONS_MODEL``
--------------------------

``Default='notifications.models.Notification'``

This setting is used override the default database Model for saving notifications. Most users wouldn't need to override this
but it can be useful if you're trying to integrate django-notifs into an existing project that already has it's own Notificaiton model



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

The maximum number of retries for a notification

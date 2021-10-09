Usage
************

.. _you'd normally do: http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
.. _Celery settings in the repo: https://github.com/danidee10/django-notifs/blob/master/notifs/settings.py


Quick start
-----------

To Create/Send a notification import the notify function and call it with the following arguments::

    from notifications.utils import notify

    notify(
        **notification_kwargs,  # Notification kwargs that map to the current Notification model
        silent=True,  # Don't persist to the database
        countdown=0  # delay (in seconds) before sending the notification
        channels=('email', 'slack'),
        extra_data={
            'context': {}  # Context for the specified Notification channels
        }
    )

This example creates a *silent* notification and delivers it via ``email`` and ``slack``.

This assumes that you've implemented these channels

A `NotificationChannel` is a class thats builds a payload from a Notification object and sends it to one or more providers.
Below is an example of a channel that builds a payload containing the context and provider and then,
delivers it to the inbuilt Console provider (which simply prints out any payload that it receives)::

    from notifications.channels import BaseNotificationChannel


    class CustomNotificationChannel(BaseNotificationChannel):
        name = 'custom_notification_channel'
        providers = ['console']

        def build_payload(self, provider):
            return {'context': self.context, 'payload': provider}


.. note::
    The ``build_payload`` method accepts the current provider as an argument so you can return a different payload
    based on the current provider.


Then you can instantiate the Notification channel directly::

    console_notification = ConsoleNotificationChannel(
        notification: Notification, context={'arbitrary_data': 'data'}
    )
    console_notification.notify()  # Send immediately
    console_notification.notify(countdown=60)  # Send after 1 minute


This gives you more flexibility over the ``notify`` utility function because you can create several notifications
and decide how each individual notification should be sent


.. note::
    Notification channels are automatically registered by django-notifs
    You must inherit from the base class and specify the ``name`` property for the channel to be properly registered


Bulk sending
------------

You can send bulk notifications by setting the ``bulk`` property to ``True`` in the context dictionary::

    console_notification = ConsoleNotificationChannel(
        notification: Notification, context={'bulk': True, 'arbitrary_data': 'data'}
    )
    console_notification.notify()
    console_notification.notify(countdown=60)

or::

    notify(
        ...,
        extra_data={
            'context': {
                'bulk': True,
            }
        }
    )

.. note::
    The provider takes care of sending the payload in the most efficient way.
    (Some providers like ``pusher`` have a bulk api for delivering multiple notifications in a single batch).


Notification Model
-----------------

Django notifs includes an inbuilt notification model with the following fields:

* **source: A ForeignKey to Django's User model (optional if it's not a User to User Notification).**
* **source_display_name: A User Friendly name for the source of the notification.**
- **recipient: The Recipient of the notification. It's a ForeignKey to Django's User model.**
- **category: Arbitrary category that can be used to group messages.**
- **action: Verbal action for the notification E.g Sent, Cancelled, Bought e.t.c**
- **obj: An arbitrary object associated with the notification using the `contenttypes` app (optional).**
- **short_description: The body of the notification.**
- **url: The url of the object associated with the notification (optional).**
- **silent: If this Value is set, the notification won't be persisted to the database.**
* **extra_data: Arbitrary data as in a JSONField.**
* **channels: Notification channels related to the notification (Tuple/List in a JSONField)**

The values of the fields can easily be used to construct the notification message.


Extra/Arbitrary Data
--------------------

Besides the standard fields, django-notifs allows you to attach arbitrary data (as JSON) to a notification.
Simply pass in a dictionary as the extra_data argument.

.. note::
    This field is only persisted to the database if you use use the default Notification model or a custom model
    that provides an ``extra_data`` field.


Sending notifications asynchronously
------------------------------------

``django-notifs`` is designed to support different backends for delivering notifications.
By default it uses the ``Synchronous`` backend which delivers notifications synchronously.

.. note::
   The Synchronous backend is not suitable for production because it blocks the request.
   It's more suitable for testing and debugging.
   To deliver notification asynchronously, please see the :doc:`backends section <./backends>`.


Delayed notifications
-------------------------------
You can delay a notification by passing the ``countdown`` (in seconds) parameter to the ``notify`` function::

    # delay notification for one minute
    notify(**kwargs, countdown=60)


Reading notifications
---------------------

To read a notification use the read method::

    from notifications.utils import read

    # id of the notification object, you can easily pass this through a URL
    notify_id = request.GET.get('notify_id')

    # Read notification
    if notify_id:
        read(notify_id=notify_id, recipient=request.user)

.. note::
    It's really important to pass the correct recipient to the ``read`` function.

    Internally,it's used to check if the user has the right to read the notification.
    If you pass in the wrong recipient or you omit it entirely, ``django-notifs`` will raise a
    ``NotificationError``

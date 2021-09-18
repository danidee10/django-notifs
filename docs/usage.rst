Usage
************

.. _you'd normally do: http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
.. _Celery settings in the repo: https://github.com/danidee10/django-notifs/blob/master/notifs/settings.py


Quick start
-----------

To Create/Send a notification import the notify function and call it with the following arguments::

    from notifications.utils import notify

    kwargs = {
        'source': self.request.user,
        'source_display_name': self.request.user.get_full_name(),
        'recipient': recipent_user, 'category': 'Chat',
        'action': 'Sent', 'obj': message.id,
        'short_description': 'You a new message', 'url': url,
        'channels': ('email', 'websocket', 'slack'), 'silent': True,
        'content_object': self.request.user
    }
    notify(**kwargs)

This example creates a *silent* notification and delivers it via ``email``, ``websocket`` and ``slack``.

This assumes that you've implemented those channels and added them to the ``settings.NOTIFICATIONS_CHANNELS`` dictionary.


Notification Fields
-------------------

The fields in the `args` dictionary map to the fields in the `Notification` model

- **source: A ForeignKey to Django's User model (optional if it's not a User to User Notification).**
- **source_display_name: A User Friendly name for the source of the notification.**
- **recipient: The Recipient of the notification. It's a ForeignKey to Django's User model.**
- **category: Arbitrary category that can be used to group messages.**
- **action: Verbal action for the notification E.g Sent, Cancelled, Bought e.t.c**
- **obj: An arbitrary object associated with the notification using the `contenttypes` app (optional).**
- **short_description: The body of the notification.**
- **url: The url of the object associated with the notification (optional).**
- **silent: If this Value is set, the notification won't be persisted to the database.**
- **extra_data: Arbitrary data as a dictionary.**
- **channels: Delivery channels that should be used to deliver the message (Tuple/List)**

The values of the fields can easily be used to construct the notification message.


Extra/Arbitrary Data
--------------------

Besides the standard fields, django-notifs allows you to attach arbitrary data to a notification.
Simply pass in a dictionary as the extra_data argument.

.. note::
    The dictionary is serialized using python's json module so make sure the dictionary contains objects that can be serialized by the json module


Writing custom delivery channels
--------------------------------

django-notifs doesn't just allow you to send in-app notifications. you can also send external notifications 
(Like Emails and SMS) with custom delivery channels. A delivery channel is a python class that provides two methods:

1. ``construct_message`` to construct the message.

2. ``notify`` does the actual sending of the message.

There's a base meta class you can inherit. This is an example of an email delivery channel using `django.core.mail.send_mail`::

    from django.core.mail import send_mail
    from notifications.channels import BaseNotificationChannel


    class EmailNotificationChannel(BaseNotificationChannel):
        """Allows notifications to be sent via email to users."""

        def construct_message(self):
            """Constructs a message from notification arguments."""
            kwargs = self.notification_kwargs
            category = kwargs.get('category', None)
            short_description = kwargs.get('short_description', None)

            message = '{} {} {}'.format(
                kwargs['source_display_name'], kwargs['action'],
                short_description
            )

            return message

        def notify(self, message):
            """Send the notification."""
            subject = 'Notification'
            from_email = 'your@email.com'
            recipient_list = ['example@gmail.com']

            send_mail(subject, message, from_email, recipient_list)

Finally don't forget to tell `django-notifs` about your new Delivery Channel by setting::

    NOTIFICATIONS_CHANNELS = {
        'email': 'path.to.EmailNotificationChannel'
    }


Sending notifications asynchronously
------------------------------------

``django-notifs`` is designed to support different backends for delivering notifications.
By default it uses the ``Synchronous`` backend which delivers notifications synchronously.

.. note::
   The Synchronous backend is not suitable for production because it blocks the request.
   It's more suitable for testing and debugging.
   To deliver notification asynchronously, please see the :doc:`backends section <./backends>`.


Delayed/Tentative notifications
-------------------------------
You can delay a notification by passing the ``countdown`` (in seconds) parameter to the ``notify`` function

example::

    # delay notification for one minute
    notify(**kwargs, countdown=60)

A tentative notification is a conditional notification that should only be sent if a criteria is met.

An example is sending a notification if a user hasn't read a chat message in 30 minutes (as a reminder).

You can acheive this by combining the ``countdown`` functionality with some simple logic in your notification
channel class::

    # delay notification for 30 minutes
    notify(**kwargs, countdown=1800)

Delayed notification channel class::

    from notifications.channels import BaseNotificationChannel


    class DelayedNotificationChannel(BaseNotificationChannel):

        def notify(self, message):
            """Cancel the delivery if the notification has been read"""
            # notification_id is only available if the notification isn't silent
            if self.notification_id:
                notification = self.NotificationModel.objects.get(id=self.notification_id)

                if notification.read is True:
                    return

            # send the notification
            print(message)

In this example, we abort the notification if the notification has been read but you're free
to use any condition/custom logic


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

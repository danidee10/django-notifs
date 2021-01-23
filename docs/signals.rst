Signals
*******

.. warning::
   This functionality has been deperecated in favour of pure python functions

To Create/Send a notification import the notify signal and send it with the following arguments::

    from notifications.signals import notify

    kwargs = {
        'source': self.request.user,
        'source_display_name': self.request.user.get_full_name(),
        'recipient': recipent_user, 'category': 'Chat',
        'action': 'Sent', 'obj': message.id,
        'short_description': 'You a new message', 'url': url,
        'channels': ('email', 'websocket', 'slack'), 'silent': True
    }
    notify.send(sender=self.__class__, **kwargs)

To Read a notification use this::

    from notifications.signals import read

    # id of the notification object, you can easily pass this through a URL
    notify_id = request.GET.get('notify_id')

    # Read notification
    if notify_id:
        read.send(
            sender=self.__class__, notify_id=notify_id,
            recipient=request.user
        )

It's really important to pass the correct recipient to the read signal, Internally it's used to check if the user has the right to read the notification. If you pass in the wrong recipient or you omit it entirely, `django-notifs` would raise a
``NotificationError``

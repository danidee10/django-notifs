Providers
**************

.. _documentation: https://channels.readthedocs.io/en/stable/index.html
.. _channels deployment documentation: https://channels.readthedocs.io/en/stable/deploying.html

Django notifs comes with a set of inbuilt providers. These providers are typically classes that accept a payload
and contain the logic for delivery that payload to an external service.

Below are the list of supported providers:


Email
=====

The email provider uses the standard ``django.core.mail`` module.
This opens up support for multiple ESP's (Mailjet, Mailchimp, sendgrid etc)

name: ``'email'``


Installation
------------

Optional dependency for django-anymail::

    pip install django-notifs[anymail]


Settings
--------

If you use ``django-anymail`` or a custom Email backend, all you have to do configure the settings as you'd
normally do and the email provider should pick it up.


Payload
-------

Single::

    {
        'subject': 'The subject line of the email',
        'body': 'The body text. This should be a plain text message',
        'from_email': 'The sender’s address',
        'to': 'A list or tuple of recipient addresses',
        'bcc': 'A list or tuple of addresses used in the “Bcc” header when sending the email',
        'attachments': 'A list of attachments to put on the message',
        'headers': 'A dictionary of extra headers to put on the message'.
        'cc': 'A list or tuple of recipient addresses used in the “Cc” header when sending the email',
        'reply_to': 'A list or tuple of recipient addresses used in the “Reply-To” header when sending the email',
        **extra_esp,

    }

``extra_esp`` is any extra data that you want to pass to your custom Email backend.


|
|


Slack
=====

name: ``'slack'``


Installation
------------

::

    pip install django-notifs[slack]

Settings
--------

::

    NOTIFICATIONS_SLACK_BOT_TOKEN=xxxxxxx

Payload
-------

Single::

    {
        'channel': '#slack-channel-name',
        'text': 'message',
    }


|
|

Pusher Channels
===============

name: ``'pusher_channels'``

Installation
------------

::

    pip install django-notifs[pusher_channels]

Settings
--------

::

    NOTIFICATIONS_PUSHER_CHANNELS_URL=https://<app_id>:<app_secret>@api-eu.pusher.com/apps/0000000

Payload
-------

Single::

    {
        'channel': 'channel_name',
        'name': 'event_name',
        'data': {},
    }

|
|

FCM (Firebase Web push)
=======================

name: ``'fcm_web'``

Settings
--------

::

    NOTIFICATIONS_FCM_KEY=xxxxxxx

Payload
-------

Single::

    {
        'title': 'notification title',
        'body': 'body',
        'click_action': 'https://example.com',
        'icon': 'icon,
        'to': 'user_token',
    }

|
|

django-channels
===============

name: ``'django_channels'``

Installation
------------

::

    pip install django-notifs[channels]

Settings
--------

``NOTIFICATIONS_WEBSOCKET_EVENT_NAME``
--------------------------------------

``Default='notifs_websocket_message'``

The ``type`` value of the messages that are going to received by the django notifs websocket consumer.
In most cases, you don't need to change this setting.

``NOTIFICATIONS_WEBSOCKET_URL_PARAM``
--------------------------------------

``Default = 'room_name'``

The WebSocket URL param name.
It's also used to construct the WebSocket URL.
See the :ref:`Advanced usage <Notification channels>` section for more information.

Context
-------
::

    {
        'destination': 'Group/channel name'
    }


Payload
-------

Single::

    {
        'type': settings.NOTIFICATIONS_WEBSOCKET_EVENT_NAME,  # or a custom event name
        'message': {},
    }

Writing custom Providers
========================

Sometimes, the inbuilt providers are not sufficient to handle every use case.

You can create a custom provider by inheriting from the Base provider class or an existing Provider and Implementing the
``send`` and ``send_bulk`` method.

The Notification context is also available as a property (``self.context``)::

    from notifications.providers import BaseNotificationProvider

    class CustomNotificationProvider(BaseNotificationProvider):
        name = 'custom_provider'

        def send(self, payload):
            # call an external API?
            pass

        def send_bulk(self, payloads):
            for payload in payloads:
                self.send(payload)

            # or call an external bulk API?

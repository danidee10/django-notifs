Providers
**************

.. module:: notifications.providers

.. _django-sms: https://django-sms.readthedocs.io/en/stable/
.. _django-sms documentation: https://django-sms.readthedocs.io/en/stable/

Django notifs comes with a set of inbuilt providers. These providers are typically classes that accept a payload
and contain the logic for delivering the payload to an external service.

Below are the list of supported providers:


Email
=====

.. autoclass:: EmailNotificationProvider

name: ``'email'``

The email provider uses the standard ``django.core.mail`` module.
This opens up support for multiple ESP's (Mailjet, Mailchimp, sendgrid etc)


Installation
------------

Optional dependency for django-anymail::

    pip install django-notifs[anymail]


Settings
--------

If you use ``django-anymail`` or a custom Email backend, all you have to do configure the settings and dependencies as you'd
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

SMS (with django-sms)
=====================

.. autoclass:: DjangoSMSNotificationProvider

name: ``'django_sms'``

The SMS provider uses a third-party app called `django-sms`_ this also, opens up support for multiple SMS providers:

Supported providers are:

* Twilio
* Message bird


Installation
------------

::

    pip install django-notifs[sms]

Extra dependencies can be installed by::

    pip install django-sms[twilio,messagebird]

Settings
--------

See the `django-sms documentation`_ for more information on how to configure your preferred backend. Once it is configured,
django-notifs should pick it up

Payload
-------

Single::

    {
        'body': 'Sample message',
        'originator': '+10000000000',
        'recipients': ['+20000000000', '+30000000000']  # list of recipients
    }

|

Slack
=====

.. autoclass:: SlackNotificationProvider

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

Pusher Channels
===============

.. autoclass:: PusherChannelsNotificationProvider

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

FCM (Firebase Web push)
=======================

.. autoclass:: FCMWebNotificationProvider

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

django-channels
===============

.. autoclass:: DjangoChannelsNotificationProvider

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

|
|

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

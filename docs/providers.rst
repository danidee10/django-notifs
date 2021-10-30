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

.. autopydantic_model:: notifications.providers.email.EmailSchema

You can still pass extra keyword arguments like ``tags`` (*depending on the ESP that you use.*)
See the ``django-anymail`` `documentation <https://anymail.readthedocs.io/>`_ for more information.

|

SMS (with django-sms)
=====================

.. autoclass:: DjangoSMSNotificationProvider

name: ``'django_sms'``

The SMS provider uses a third-party app called `django-sms`_ this also opens up support for multiple SMS providers.

Supported providers are:

* Twilio
* Message bird


Installation
------------

::

    pip install django-notifs[django_sms]

Extra dependencies can be installed by::

    pip install django-sms[twilio,messagebird]

Settings
--------

See the `django-sms documentation`_ for more information on how to configure your preferred backend. Once it is configured,
``django-notifs`` should pick it up

Payload
-------

.. autopydantic_model:: notifications.providers.django_sms.DjangoSmsSchema

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

.. autopydantic_model:: notifications.providers.slack.SlackSchema

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

.. autopydantic_model:: notifications.providers.pusher_channels.PusherChannelsSchema

|

FCM (Firebase Web push)
=======================

.. autoclass:: FCMWebNotificationProvider

name: ``'fcm_web'``

Settings
--------

::

    NOTIFICATIONS_FCM_WEB_API_KEY=xxxxxxx  # FCM Api key
    NOTIFICATIONS_FCM_WEB_PROXY = {}  # FCM proxy

Payload
-------

Single:

.. autopydantic_model:: notifications.providers.fcm_web.FCMWebSchema

Bulk:

.. autopydantic_model:: notifications.providers.fcm_web.BulkFCMWebSchema

|

Twitter status update
=====================

django-notifs uses `tweepy <https://docs.tweepy.org/en/stable>`_ to deliver twitter notifiations

.. autoclass:: TwitterStatusUpdateNotificationProvider

name: ``'twitter_status_update'``

Installation
------------

::

    pip install django-notifs[twitter]

Settings
--------

``NOTIFICATIONS_TWITTER_CONSUMER_KEY``
--------------------------------------

Twitter consumer key

``NOTIFICATIONS_TWITTER_CONSUMER_SECRET``
-----------------------------------------

Twitter consumer secret

``NOTIFICATIONS_TWITTER_ACCESS_TOKEN``
--------------------------------------

Twitter access token

``NOTIFICATIONS_TWITTER_ACCESS_TOKEN_SECRET``
---------------------------------------------

Twitter access token secret


Payload
-------

.. autopydantic_model:: notifications.providers.twitter_status_update.TwitterStatusUpdateSchema

See the `tweepy documentation <https://docs.tweepy.org/en/stable/api.html?highlight=status_update#tweepy.API.update_status>`_
for more information on these parameters

|
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
        'channel_layer': "Custom django channels layer or 'default'",
        'destination': 'Group/channel name'
    }


Payload
-------

.. autopydantic_model:: notifications.providers.django_channels.DjangoChannelsSchema

|
|

Writing custom Providers
========================

Sometimes, the inbuilt providers are not sufficient to handle every use case.

You can create a custom provider by inheriting from the Base provider class or an existing Provider and Implementing the
``get_validator``/``validate``, ``send`` and ``send_bulk`` method.

The Notification context is also available as a property (``self.context``)::

    from typing import Dict, List

    from pydantic import BaseModel

    from notifications.providers import BaseNotificationProvider


    class CustomProviderSchema(BaseModel):
        event: str
        message: Dict

    
    class BulkCustomProviderSchema(BaseModel):
        group: str
        messages: List[CustomProviderSchema]


    class CustomNotificationProvider(BaseNotificationProvider):
        name = 'custom_provider'
        validator = CustomProviderSchema

        def get_validator(self):
            """Return a custom validator based on the context."""
            if self.context.get('bulk', False) is True:
                return BulkCustomProviderSchema

            return CustomProviderSchema

        def validate(self, payload):
            """Validate without pydantic."""
            pass

        def send(self, payload):
            # call an external API?
            pass

        def send_bulk(self, payloads):
            for payload in payloads:
                self.send(payload)

            # or call an external bulk API?

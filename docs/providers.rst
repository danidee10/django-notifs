Providers
**************

.. _documentation: https://channels.readthedocs.io/en/stable/index.html
.. _channels deployment documentation: https://channels.readthedocs.io/en/stable/deploying.html

Django notifs comes with a set of inbuilt providers. These providers are typically classes that accept a payload
and contain the logic for delivery that payload to an external service.

Below are the list of supported providers:

``Slack``
---------

settings::

    NOTIFICATIONS_SLACK_BOT_TOKEN  # Slack notification bot token

Single payload::

    {
        'channel': '#slack-channel-name',
        'text': 'message',
    }

Pusher,
Google FCM,
django-channels,

Writing custom Providers
--------------------------------

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

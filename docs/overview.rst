Overview
********

Requirements
------------

    * Python 3.6+
    * Django 2.2+

Supported Functionality
-----------------------

    * In-app notifications
    * Silent notifications (i.e Notifications that aren't saved in the database)
    * Delivery providers e.g Email, Slack, SMS etc
    * Custom delivery channels and providers
    * Asynchronous notifications (with support for multiple backends e.g Celery, RQ, AwsLambda etc)

Supported providers
-------------------
    * :ref:`Email <Email>`: SMTP and Transaction email providers (Amazon SES, Mailgun, Mailjet, Postmark, SendinBlue, SendGrid, SparkPost and Mandrill) with `django-anymail <https://anymail.readthedocs.io/>`_
    * :ref:`SMS <SMS (with django-sms)>`: (Twilio, Messagebird) with `django-sms <https://django-sms.readthedocs.io/en/latest/>`_
    * :ref:`Slack <Slack>`
    * :ref:`Pusher Channels <Pusher Channels>`
    * :ref:`FCM - Web push notifications (*deprecated*) <FCM (Firebase Web push)>`
    * :ref:`Django channels <django-channels>`
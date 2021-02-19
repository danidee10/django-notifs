[![Documentation](https://readthedocs.org/projects/django-notifs/badge/)](https://django-notifs.readthedocs.io)
[![Maintainability](https://api.codeclimate.com/v1/badges/3f5dd1e1833c12c79db9/maintainability)](https://codeclimate.com/github/danidee10/django-notifs/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/3f5dd1e1833c12c79db9/test_coverage)](https://codeclimate.com/github/danidee10/django-notifs/test_coverage)
[![Pypi](https://img.shields.io/pypi/v/django-notifs.svg)](https://pypi.python.org/pypi/django-notifs)
[![Style guide](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)

<h3>Modular Notifications (InApp, Email, SMS, CustomBackend etc) for Django</h3>

![django-notifs](./django-notifs.png)

django-notifs is a modular notifications app for Django that basically allows you to notify users about events that occur in your application E.g

- Your profile has been verified
- User xxxx sent you a message

It also allows you to deliver these notifications to any destination you want to with custom delivery channels.

It also supports asynchronous notification with several pluggable delivery backends (e.g Celery, RQ etc)

#### Examples?

A tutorial on how to build a [Realtime Chat application with Vue, django-notifs, RabbitMQ and uWSGI](https://danidee10.github.io/2018/01/01/realtime-django-1.html)

The Repository for the chat app (Chatire) is also available on [github](https://github.com/danidee10/chatire)


#### Documentation
https://django-notifs.readthedocs.io

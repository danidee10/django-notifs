Installation
************

Get it from pip with::

    pip install django-notifs

Include it in ``settings.INSTALLED_APPS``::

    INSTALLED_APPS = (
        'django.contrib.auth',
        ...
        'notifications',
        'django_jsonfield_backport'  # if you're running django < 3.1
        ...
    )

Finally don't forget to run the migrations with::

    python manage.py migrate notifications


You can also register the current Notification model in django admin::

    """admin.py file."""
    from django.contrib import admin
    from .utils import get_notification_model


    Notification = get_notification_model()
    admin.site.register(Notification)

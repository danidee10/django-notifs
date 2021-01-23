Installation
************

Get it from pip with::

    pip install django-notifs

Include it in ``settings.INSTALLED_APPS``::

    INSTALLED_APPS = (
        'django.contrib.auth',
        ...
        'notifications',
        ...
    )

Include the urls in urls.py::

    urlpatterns = [
        ...
        path('notifications/', include('notifications.urls', namespace='notifications')),
        ...
    ]

Finally don't forget to run the migrations with::

    python manage.py migrate notifications

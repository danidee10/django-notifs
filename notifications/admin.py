"""admin.py file."""

from django.contrib import admin

from .utils import get_notification_model


Notification = get_notification_model()


admin.site.register(Notification)

"""Notification model."""

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .fields import JSONField


class NotificationQuerySet(models.QuerySet):
    """Notifications QuerySet."""

    def all_unread(self):
        """Return all unread notifications."""

        return self.filter(is_read=False)

    def all_read(self):
        """Return all read notifications."""

        return self.filter(is_read=True)


class BaseNotificationModel(models.Model):
    """
    Model for notifications.

    Parameters:
    ----------
    source: A ForeignKey to Django's User model
        (Can be null if it's not a User to User Notification)

    source_display_name: A User Friendly name
        for the source of the notification.

    recipient: The Recipient of the notification.
        It's a ForeignKey to Django's User model.

    action: Verbal action for the notification
        E.g Sent, Cancelled, Bought e.t.c

    obj: The id of the object associated with the notification
        (Can be null)

    short_description: The body of the notification.

    url: The url of the object associated with the notification
        (Can be null)
    channels: Channel(s) that were/was used to deliver the message

    extra_data: Extra information that was passed in the notification
        (Optional but default value is an empty dict {})
    """

    User = settings.AUTH_USER_MODEL

    class Meta:
        ordering = ('-id',)
        abstract = True

    source = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    source_display_name = models.CharField(max_length=150, null=True)
    recipient = models.ForeignKey(
        User, related_name='notifs_notifications', null=True, on_delete=models.CASCADE
    )
    action = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    obj = GenericForeignKey('content_type', 'object_id')

    url = models.URLField(null=True, blank=True)
    short_description = models.CharField(max_length=100)
    channels = JSONField(default=list)
    extra_data = JSONField(default=dict)
    is_read = models.BooleanField(default=False)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # register queryset
    objects = NotificationQuerySet.as_manager()

    def __str__(self):
        if self.source:
            res = '{}: {} {} {} => {}'.format(
                self.category,
                self.source,
                self.action,
                self.short_description,
                self.recipient,
            )
        else:
            res = self.short_description

        return res

    def read(self):
        """Mark notification as read."""
        self.is_read = True
        self.save()

    def to_json(self):
        """
        Return JSON representation that can easily be serialized."""
        return {
            'notification_id': self.id,
            'source': getattr(self.source, 'id', ''),
            'source_display_name': self.source_display_name,
            'recipient': getattr(self.recipient, 'id', ''),
            'category': self.category,
            'action': self.action,
            'obj': self.obj,
            'short_description': self.short_description,
            'url': self.url,
            'channels': self.channels,
            'extra_data': self.extra_data,
            'is_read': self.is_read,
        }


class Notification(BaseNotificationModel):
    pass

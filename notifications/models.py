"""Notification model."""

from django.db import models
from django.contrib.auth.models import User

class NotificationManager(models.Manager):
    """Custom manager to add extra functionality."""

    def unread(self):
        """Return all unread notifications."""
        queryset = self.get_queryset()

        return queryset.filter(is_read=False)


class Notification(models.Model):
    """Model for notifications."""

    class Meta:
        """Specify ordering for objects."""
        ordering = ('-id',)

    source = models.ForeignKey(User, null=True)
    source_display_name = models.CharField(max_length=150, null=True)
    recipent = models.ForeignKey(User, related_name='notifications')
    action = models.CharField(max_length=50)  # e.g 'Created'
    category = models.CharField(max_length=50)
    obj = models.IntegerField()  # id of the object
    url = models.URLField()  # by default is absolute_url of the object
    is_read = models.BooleanField(default=False)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # e.g 'a New Quote'
    short_description = models.CharField(max_length=100)

    # register queryset
    objects = NotificationManager()

    def __str__(self):
        if self.source:
            res = '{}: {} {} {} => {}'.format(
                self.category, self.source, self.action,
                self.short_description, self.recipent
            )
        else:
            res = self.short_description

        return res

    def read(self):
        """Mark notification as read."""
        self.is_read = True
        self.save()

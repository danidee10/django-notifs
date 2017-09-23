"""Notification model."""

from django.db import models
from django.contrib.auth.models import User


class NotificationQuerySet(models.QuerySet):
    """Notifications QuerySet."""

    def all_unread(self):
        """Return all unread notifications."""

        return self.filter(is_read=False)

    def all_read(self):
        """Return all read notifications."""

        return self.filter(is_read=True)


class Notification(models.Model):
    """Model for notifications."""

    class Meta:
        """Specify ordering for objects."""
        ordering = ('-id',)

    source = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    source_display_name = models.CharField(max_length=150, null=True)
    recipent = models.ForeignKey(
        User, related_name='notifications', on_delete=models.CASCADE
        )
    action = models.CharField(max_length=50)  # e.g 'Created'
    category = models.CharField(max_length=50)
    obj = models.IntegerField()  # id of the object
    url = models.URLField()  # url of the object (E.g calling obj.absolute_url)
    is_read = models.BooleanField(default=False)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # e.g 'a New Quote'
    short_description = models.CharField(max_length=100)

    # register queryset
    objects = NotificationQuerySet.as_manager()

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

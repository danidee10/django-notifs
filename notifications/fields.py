"""Custom model fields."""

from django.db import models

from django_jsonfield_backport.models import JSONField  # noqa


class ListField(models.CharField):
    """
    Emulate django.contrib.postgres ArrayField.

    Deprecated in favour of JSONField. It's just here for old migrations
    """

    def get_prep_value(self, value):
        """Convert the list/tuple to a comma separated string."""
        super(ListField, self).get_prep_value(value)

        if not value:
            return value

        return ','.join(value)

    def from_db_value(self, value, expression, connection):
        """Return the value from the database as a python list."""
        if not value:
            return []

        return value.split(',')

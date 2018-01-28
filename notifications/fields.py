"""Custom model fields."""

import json
from django.db import models


class JSONField(models.TextField):
    """Add's JSON capablilties (retrieval) to Django's TextField."""

    def get_prep_value(self, value):
        """Convert the dictionary to JSON, which is saved as text."""
        db_value = super(JSONField, self).get_prep_value(value)

        return json.dumps(db_value)

    def from_db_value(self, value, expression, connection, *args, **kwargs):
        """Convert the JSON back to a dictionary."""
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    def to_python(self, value):
        """Simply returns the dictionary"""
        return value


class ListField(models.CharField):
    """Emulate django.contrib.postgres ArrayField."""

    def get_prep_value(self, value):
        """Convert the list/tuple to a comma separated string."""
        super(ListField, self).get_prep_value(value)

        return ','.join(value)

    def from_db_value(self, value, expression, connection, *args, **kwargs):
        """Return the value from the database as a python list."""

        return value.split(',')

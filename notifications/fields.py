"""Custom model fields."""

import ast
import json
from django.db import models


class JSONField(models.TextField):
    """Add's JSON capablilties (retrieval) to Django's TextField."""

    def get_prep_value(self, value):
        """Convert the dictionary to JSON, which is saved as text."""
        db_value = super().get_prep_value(value)

        return json.dumps(db_value)

    def from_db_value(self, value, expression, connection):
        """Convert the JSON back to a dictionary."""
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    def to_python(self, value):
        """Simply returns the dictionary"""
        return value

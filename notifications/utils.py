"""Utilities and helper functions."""

import importlib

from . import default_settings as settings


def import_channel(channel_alias):
    """
    helper to import channels aliases from string paths.
  
    raises an AttributeError if a channel can't be found by it's alias
    """

    try:
        channel_path = settings.NOTIFICATIONS_CHANNELS[channel_alias]
    except KeyError:
        raise AttributeError(
            '"%s" is not a valid delivery channel alias. '
            'Check your applications settings for NOTIFICATIONS_CHANNELS'
            % channel_alias
        )

    package, attr = channel_path.rsplit('.', 1)

    return getattr(importlib.import_module(package), attr)

"Utility functions"

from ..utils import _import_class_string, _validate_channel_alias


def _send_notification(notification, logger):
    """Instantiates the notification channels and calls 'notify'."""
    for channel_alias in notification['channels']:
        # Validate channel alias
        channel_path = _validate_channel_alias(channel_alias)

        channel = _import_class_string(channel_path)(
            **notification, alias=channel_alias
        )

        message = channel.construct_message()
        channel.notify(message)
        logger.info(
            'Sent notification with the %s channel. kwargs: %s\n' %
            (channel_alias, notification)
        )

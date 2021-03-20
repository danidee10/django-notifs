"Utility functions"


def _send_notification(notification, channel_alias, logger):
    # prevent `AppRegistryNotReady Exception`
    from ..utils import _import_class_string, _validate_channel_alias

    """Instantiates the notif-channel and calls it's 'notify' method."""
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

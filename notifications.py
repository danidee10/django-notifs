"""Custom context processor.

To include the notifications varialbe in all templates
"""


def notifications(request):
    """Get the total number of unread notifications for authenticated users."""
    if not request.user.is_authenticated:
        return {}

    return {'notifications': request.user.notifications}

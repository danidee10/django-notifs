"""
Context Processor

To include the notifications varialbe in all templates.
"""


def notifications(request):
    """Make notifications available in all templates."""
    if not request.user.is_authenticated:
        return {}

    return {'notifications': request.user.notifications}

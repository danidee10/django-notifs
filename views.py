from django.shortcuts import render
from django.views.generic import ListView

from .models import Notification

class NotificationsView(ListView):
    """View for notifications for clients/mechanics."""

    model = Notification

    def get_queryset(self):
        """Filter notifications by currently logged in user."""
        queryset = super().get_queryset()

        return queryset.filter(recipent=self.request.user)

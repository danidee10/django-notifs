"""views.py."""

import pika
from json import loads

from django.conf import settings
from django.http import JsonResponse
from django.views.generic import ListView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Notification


class NotificationsView(ListView):
    """View for notifications for clients/mechanics."""

    model = Notification
    context_object_name = 'notifications_list'

    paginate_by = getattr(settings, 'PAGINATE_BY', None)

    def get_queryset(self):
        """Filter notifications by currently logged in user."""
        queryset = super().get_queryset()

        return queryset.filter(recipient=self.request.user)


class GenerateNotification(View):
    """View to generate test notifications."""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """disable CSRF Verification."""
        return super().dispatch(request, *args, **kwargs)

    def add_access_control_headers(self, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

    def post(self, request, *args, **kwargs):
        """Generate the notification."""
        data = loads(request.body)
        message = data['message']

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='notifications')

        channel.basic_publish(
            exchange='', routing_key='notifications', body=message
        )
        print("Sent '{}'".format(message))

        connection.close()

        response = JsonResponse({'message': 'Notification generated'})

        self.add_access_control_headers(response)

        return response

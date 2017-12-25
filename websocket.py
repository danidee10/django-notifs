"""
Implements a websocket based on uWSGI

Consumes messages from a RabbitMQ Queue.
"""

import sys

import pika
import uwsgi

import django
from django.conf import settings


# Setup Django and load apps
django.setup()

RABBIT_MQ_URL = getattr(
    settings, 'NOTIFICATIONS_RABBIT_MQ_URL', 'amqp://guest:guest@localhost:5672'
)


def application(env, start_response):
    """Setup the Websocket Server and read messages off the queue."""
    connection = pika.BlockingConnection(
        pika.connection.URLParameters(RABBIT_MQ_URL)
    )
    channel = connection.channel()
   
    queue = env['PATH_INFO'].replace('/', '')
    
    channel.queue_declare(queue=queue)

    uwsgi.websocket_handshake(
        env['HTTP_SEC_WEBSOCKET_KEY'],
        env.get('HTTP_ORIGIN', '')
    )

    def keepalive():
        """Keep the websocket connection alive (called each minute)."""
        print('PING/PONG...')
        try:
            uwsgi.websocket_recv_nb()
            connection.add_timeout(60, keepalive)
        except OSError as error:
            print('Killing the connection...')
            sys.exit(0)

    def callback(ch, method, properties, body):
        """Callback called when a message has been received."""
        try:
            uwsgi.websocket_send(body)
        except OSError as error:
            print('Could not send message over the websocket', error)
            sys.exit(0)

    keepalive()
    channel.basic_consume(callback, queue=queue, no_ack=True)
    channel.start_consuming()

"""
Implements a websocket based on uWSGI

Consumes messages from a RabbitMQ Queue.
"""

import sys

import pika
import uwsgi

import django

import notifications.default_settings as settings


# Setup Django and load apps
django.setup()


def application(env, start_response):
    """Setup the Websocket Server and read messages off the queue."""
    rabbit_mq_url = settings.NOTIFICATIONS_RABBIT_MQ_URL
    connection = pika.BlockingConnection(
        pika.connection.URLParameters(rabbit_mq_url)
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
            connection.add_timeout(30, keepalive)
        except OSError as error:
            print(error)
            sys.exit(1) # Kill process and force uWSGI to Respawn

    keepalive()

    while True:
        for method_frame, _, body in channel.consume(queue):
            try:
                uwsgi.websocket_send(body)
            except OSError as error:
                print(error)
                sys.exit(1) # Kill process and force uWSGI to Respawn
            else:
                # acknowledge the message
                channel.basic_ack(method_frame.delivery_tag)

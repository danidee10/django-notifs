"""
Implements a websocket based on uWSGI

Consumes messages from a RabbitMQ Queue.
"""

import pika
import uwsgi

import django


# Setup Django and load apps
django.setup()


def application(env, start_response):
    """Setup the Websocket Server and read messages off the queue."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='notifications')

    uwsgi.websocket_handshake(
        env['HTTP_SEC_WEBSOCKET_KEY'],
        env.get('HTTP_ORIGIN', '')
    )

    def keepalive():
        """Keep the websocket connection alive (called each minute)."""
        print('PING/PONG...')
        uwsgi.websocket_recv_nb()
        connection.add_timeout(60, keepalive)

    def callback(ch, method, properties, body):
        """Callback called when a message has been received."""
        try:
            uwsgi.websocket_send(body)
        except OSError as error:
            print('Could not send message over the websocket', error)

    keepalive()
    channel.basic_consume(callback, queue='demouser', no_ack=True)
    channel.start_consuming()

"""General Tests."""

import os
from unittest.mock import Mock, patch

import boto3
from celery.exceptions import Retry
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from moto import mock_sqs

from ..backends import RQ, AwsSqsLambda, Celery, Channels, Console
from ..channels import DjangoWebSocketChannel
from ..consumers import DjangoNotifsConsumer
from ..tasks import consume
from ..utils import get_notification_model

Notification = get_notification_model()


class BackendTests(TestCase):
    """
    Tests for the Delivery backends

    This class also contains tests for asynchronous functions/methods
    that aren't triggered from the regular unit tests
    """

    User = get_user_model()

    @classmethod
    def setUpTestData(cls):
        """Create Users."""
        cls.user1 = cls.User.objects.create_user(
            username='user1@gmail.com', password='password'
        )

        cls.user2 = cls.User.objects.create_user(
            username='user2@gmail.com', password='password'
        )

        cls.notification = Notification(
            source=cls.user2,
            source_display_name='User 2',
            recipient=cls.user1,
            action='Notified',
            category='General notification',
            obj=cls.user2,
            url='http://example.com',
            short_description='Short Description',
            is_read=False,
        )

    def test_console_backend(self):
        websocket_channel = DjangoWebSocketChannel(
            self.notification, context={'message': {'text': 'Hello world'}}
        )
        delivery_backend = Console(websocket_channel)

        self.assertIsNone(delivery_backend.run(countdown=0))

    @override_settings(CELERY_BROKER_URL='redis://localhost:6379/0')
    def test_celery_backend(self):
        websocket_channel = DjangoWebSocketChannel(
            self.notification, context={'message': {'text': 'Hello world'}}
        )
        delivery_backend = Celery(websocket_channel)

        self.assertIsNone(delivery_backend.run(countdown=0))

    @patch('notifications.backends.celery.settings.NOTIFICATIONS_RETRY', True)
    @patch(
        'notifications.backends.celery.CeleryBackend.consume',
        Mock(side_effect=Exception),
    )
    @patch(
        'notifications.backends.celery.consume.retry',
        Mock(side_effect=Retry),
    )
    def test_celery_backend_retry(self):

        with self.assertRaises(Retry):
            consume(
                'django_channels',
                {'type': 'celery', 'message': 'Hello world'},
                context={'destination': 'celery_users'},
            )

    @override_settings(
        CHANNEL_LAYERS={
            'django_notifs': {
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                    "hosts": [('127.0.0.1', 6379)],
                },
            },
        }
    )
    def test_channels_backend(self):
        websocket_channel = DjangoWebSocketChannel(
            self.notification, context={'message': {'text': 'Hello world'}}
        )
        delivery_backend = Channels(websocket_channel)

        self.assertIsNone(delivery_backend.run(countdown=0))

    @patch('notifications.default_settings.NOTIFICATIONS_RETRY', True)
    def test_rq_backend(self):
        websocket_channel = DjangoWebSocketChannel(
            self.notification, context={'message': {'text': 'Hello world'}}
        )
        delivery_backend = RQ(websocket_channel)

        self.assertIsNone(delivery_backend.run(countdown=0))

    @mock_sqs
    def test_aws_lambda_sqs(self):
        # Create and mock SQS queue
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_SECURITY_TOKEN'] = 'testing'
        os.environ['AWS_SESSION_TOKEN'] = 'testing'
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

        sqs = boto3.client('sqs')
        lambda_queue = sqs.create_queue(QueueName='aws-lambda-example')

        with patch(
            'notifications.default_settings.NOTIFICATIONS_SQS_QUEUE_URL',
            lambda_queue['QueueUrl'],
        ):
            websocket_channel = DjangoWebSocketChannel(
                self.notification, context={'message': {'text': 'Hello world'}}
            )
            delivery_backend = AwsSqsLambda(websocket_channel)

            self.assertIsNone(delivery_backend.run(countdown=0))

    def test_celery_task(self):
        """This ensures that the Celery task runs without errors."""
        self.assertIsNone(
            consume(
                'django_channels',
                {'type': 'celery', 'message': 'Hello world'},
                context={'destination': 'celery_users'},
            )
        )

    async def test_channels_consumer(self):
        """This ensures that the Channels consumer runs without errors."""
        consumer = DjangoNotifsConsumer()
        message = {
            'provider': 'django_channels',
            'payload': {'type': 'celery', 'message': 'Hello world'},
            'context': {'destination': 'celery_users'},
            'countdown': 0,
        }
        result = await consumer.notify(message)
        self.assertIsNone(result)

"""AWS SQS backend"""

import logging
import json

import boto3

from .base import BaseBackend
from notifications import default_settings as settings


class AwsSqsLambdaBackend(BaseBackend):
    logger = logging.getLogger('django_notifs.backends.aws_sqs_lambda')

    def produce(self, provider, provider_class, payload, context, countdown):
        QUEUE_URL = settings.NOTIFICATIONS_SQS_QUEUE_URL
        SQS = boto3.client('sqs')

        message = {
            'provider': provider,
            'provider_class': provider_class,
            'payload': payload,
            'context': context
        }

        SQS.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message),
        )


class AwsSqsLambdaConsumer:

    @classmethod
    def consume(cls, event, context):
        for record in event['Records']:
            message = json.loads(record['body'])
            AwsSqsLambdaBackend.consume(**message)

"""AWS SQS backend"""

import json
import logging

import boto3

from notifications import default_settings as settings

from .base import BaseBackend


class AwsSqsLambdaBackend(BaseBackend):
    logger = logging.getLogger('django_notifs.backends.aws_sqs_lambda')

    def produce(self, provider, payload, context, countdown):
        queue_url = settings.NOTIFICATIONS_SQS_QUEUE_URL
        sqs = boto3.client('sqs')

        message = {
            'provider': provider,
            'payload': payload,
            'context': context,
        }

        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message),
            DelaySeconds=countdown,
        )


class AwsSqsLambdaConsumer:
    @classmethod
    def consume(cls, event, context):
        for record in event['Records']:
            message = json.loads(record['body'])
            AwsSqsLambdaBackend.consume(**message)

from notifications.backends.aws_sqs_lambda import AwsSqsLambdaConsumer


def consumer(event, context):
    AwsSqsLambdaConsumer.consume(event, context)

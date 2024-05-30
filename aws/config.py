import boto3
import json

config = {}
sns_client = boto3.client('sns')
response = sns_client.create_topic(Name='co2-readings')
topic_arn = response['TopicArn']

sqs_client = boto3.client('sqs')
response = sqs_client.create_queue(QueueName='small-queue')
small_queue_url = response['QueueUrl']
small_queue_attrs = sqs_client.get_queue_attributes(QueueUrl=small_queue_url, AttributeNames=['All'])['Attributes']
small_queue_arn = small_queue_attrs['QueueArn']

# Subscribe SQS queue to SNS
sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol='sqs',
    Endpoint=small_queue_arn
)

response = sqs_client.create_queue(QueueName='large-queue')
large_queue_url = response['QueueUrl']
large_queue_attrs = sqs_client.get_queue_attributes(QueueUrl=large_queue_url, AttributeNames=['All'])['Attributes']
large_queue_arn = large_queue_attrs['QueueArn']

# Subscribe SQS queue to SNS
sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol='sqs',
    Endpoint=large_queue_arn
)

response = sqs_client.create_queue(QueueName='metrics-queue')
metrics_queue_url = response['QueueUrl']
metrics_queue_attrs = sqs_client.get_queue_attributes(QueueUrl=metrics_queue_url, AttributeNames=['All'])['Attributes']
metrics_queue_arn = metrics_queue_attrs['QueueArn']

# Subscribe SQS queue to SNS
sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol='sqs',
    Endpoint=metrics_queue_arn
)

config = {
    "SNS_TOPIC_ARN": topic_arn,
    "SQS_URLS": {
        "S": small_queue_url,
        "L": large_queue_url,
        "METRICS": metrics_queue_url
    }
}

with open("config.json", "w") as file:
    json.dump(config, file)
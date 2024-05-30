import boto3
import json

config = {}
sns_client = boto3.client('sns')
response = sns_client.create_topic(Name='co2-readings')
topic_arn = response['TopicArn']

sqs_client = boto3.client('sqs')
response = sqs_client.create_queue(QueueName='small-queue')
small_queue_url = response['QueueUrl']

response = sqs_client.create_queue(QueueName='large-queue')
large_queue_url = response['QueueUrl']

response = sqs_client.create_queue(QueueName='metrics-queue')
metrics_queue_url = response['QueueUrl']

config = {
    "SNS Topic ARN": topic_arn,
    "SQS URLs": {
        "s": small_queue_url,
        "l": large_queue_url,
        "metrics": metrics_queue_url
    }
}

with open("config.json", "w") as file:
    json.dump(config, file)
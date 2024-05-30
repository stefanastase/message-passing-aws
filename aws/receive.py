import boto3
import json

sqs = boto3.client('sqs')

with open('config.json', 'r') as cfg_file:
    config = json.load(cfg_file)

QUEUE_URL_1 = config['SQS_URLS']['S']
QUEUE_URL_2 = config['SQS_URLS']['L']
QUEUE_URL_3 = config['SQS_URLS']['METRICS']

def lambda_1():
    print("Lambda 1 triggered: Opening small window")

def lambda_2():
    print("Lambda 2 triggered: Opening large window")

def process_queues():
    while True:
        response_1 = sqs.receive_message(
            QueueUrl=QUEUE_URL_1,
            MaxNumberOfMessages=3,
            WaitTimeSeconds=20
        )
        if 'Messages' in response_1 and len(response_1['Messages']) >= 3:
            lambda_1()
            for message in response_1['Messages']:
                sqs.delete_message(
                    QueueUrl=QUEUE_URL_1,
                    ReceiptHandle=message['ReceiptHandle']
                )

        response_2 = sqs.receive_message(
            QueueUrl=QUEUE_URL_2,
            MaxNumberOfMessages=8,
            WaitTimeSeconds=20
        )
        if 'Messages' in response_2 and len(response_2['Messages']) >= 5:
            lambda_2()
            for message in response_2['Messages']:
                sqs.delete_message(
                    QueueUrl=QUEUE_URL_2,
                    ReceiptHandle=message['ReceiptHandle']
                )

        response_metrics = sqs.receive_message(
            QueueUrl=QUEUE_URL_3,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10
        )
        if 'Messages' in response_metrics:
            for message in response_metrics['Messages']:
                # Process for analytics
                print("Metrics Queue Message: ", message['Body'])
                sqs.delete_message(
                    QueueUrl=QUEUE_URL_3,
                    ReceiptHandle=message['ReceiptHandle']
                )

process_queues()

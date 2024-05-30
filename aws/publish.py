import boto3
import time
import random
import json

with open('config.json', 'r') as cfg_file:
    config = json.load(cfg_file)

sns = boto3.client('sns')

SNS_TOPIC_ARN = config['SNS_TOPIC_ARN']
def publish_co2_reading():
    while True:
        co2_level = random.randint(300, 2000)  # Simulate random value for CO2 reading
        print(co2_level)
        if co2_level > 1000:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f'High CO2 detected: {co2_level}'
            )
        time.sleep(60)  # Sensor reads every minute 

publish_co2_reading()
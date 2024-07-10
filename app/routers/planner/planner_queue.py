import json
import os
import urllib.parse

import boto3

from app.schemas.planner_schemas.planner import PlanMetaData

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = urllib.parse.quote_plus(
    os.getenv("AWS_SECRET_ACCESS_KEY"), safe="/"
)
queue_url = os.getenv("QUEUE_URL")

sqs = boto3.client(
    "sqs",
    region_name="us-east-2",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)


def queue_plan(user_id: int, plan_metadata: PlanMetaData):
    message = {
        "user_id": user_id,
        "plan_name": plan_metadata.plan_name,
        "destination": plan_metadata.destination,
        "init_date": str(plan_metadata.init_date),
        "end_date": str(plan_metadata.end_date),
    }

    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message),
        MessageGroupId="planner",
    )

    print(f'Message sent: {response["MessageId"]}')

import json
import os

import boto3
from chat_downloader import ChatDownloader as cd


def lambda_handler(event, context):
    sqs = boto3.client("sqs")
    COMPREENSIONS_QUEUE_URL = os.environ.get(
        "COMPREENSIONS_QUEUE_URL",
        "https://sqs.us-east-2.amazonaws.com/211125768252/Live-Cut-The-Bullshit-Compreensions",
    )

    record = event["Records"][0]
    message = json.loads(record["Sns"]["Message"])
    
    video_id = message["video_id"]
    url = message["url"]

    chat = cd().get_chat(url)

    BATCH_SIZE = 25
    batch = []

    for message in chat:
        batch.append(
            {
                "video_id": video_id,
                "timestamp": message["timestamp"],
                "time_in_seconds": message["time_in_seconds"],
                "message": message["message"],
                "author": message["author"],
            }
        )

        if len(batch) == BATCH_SIZE:
            sqs.send_message(QueueUrl=COMPREENSIONS_QUEUE_URL, MessageBody=json.dumps({"batch": batch}))
            batch = []

    # Send the last batch
    sqs.send_message(
        QueueUrl=COMPREENSIONS_QUEUE_URL,
        MessageBody=json.dumps({"batch": batch}),
    )

import json
import math
import os
from dataclasses import dataclass
from datetime import timedelta

import boto3


@dataclass
class Input:
    pass


@dataclass
class Output:
    message: str


def convert_to_minutes(duration):
    # Split the time string into hours, minutes, and seconds
    hours, minutes, seconds = map(int, duration.split(":"))

    # Create a timedelta object
    total_duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    # Convert the total duration to minutes
    total_minutes = total_duration.total_seconds() / 60
    return total_minutes


def lambda_handler(event, context):

    video_id = event["pathParameters"]["video_id"]
    interval = event["queryStringParameters"].get("interval", 10)

    s3_client = boto3.client("s3")
    sqs = boto3.client("sqs")
    TRANSCRIPT_QUEUE_URL = os.environ.get(
        "TRANSCRIPT_QUEUE_URL", "https://sqs.us-east-2.amazonaws.com/211125768252/Dev-Transcript"
    )
    VIDEOS_TABLE_NAME = os.environ.get("VIDEOS_TABLE_NAME", "Dev-Videos")
    dynamodb = boto3.resource("dynamodb")
    videos_table = dynamodb.Table(VIDEOS_TABLE_NAME)

    video = videos_table.get_item(Key={"PK": video_id})["Item"]
    duration = video["duration"]
    duration_in_minutes = convert_to_minutes(duration)
    workers = math.ceil(duration_in_minutes / int(interval))
    TRANSCRIPTIONS_BUCKET = os.environ.get("TRANSCRIPTIONS_BUCKET", "live-cut-the-bullshit-transcriptions")

    key = f"{video_id}.json"

    response = s3_client.get_object(Bucket=TRANSCRIPTIONS_BUCKET, Key=key)
    body = json.loads(response["Body"].read())

    video_id = body["jobName"]
    transcription = body["results"]["items"]

    total_items = len(transcription)
    items_per_batch = math.ceil(total_items / workers)
    batches = [transcription[i : i + items_per_batch] for i in range(0, total_items, items_per_batch)]

    for batch in batches:
        sqs.send_message(
            QueueUrl=TRANSCRIPT_QUEUE_URL, MessageBody=json.dumps({"video_id": video_id, "transcription": batch})
        )

    return {"statusCode": 200, "body": json.dumps({"message": "ok!"}), "headers": {"Access-Control-Allow-Origin": "*"}}

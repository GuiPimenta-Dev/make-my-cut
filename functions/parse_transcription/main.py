import json
import os
import boto3
import math


def lambda_handler(event, context):

    s3_client = boto3.client("s3")
    sqs = boto3.client("sqs")
    TRANSCRIPT_QUEUE_URL = os.environ.get(
        "TRANSCRIPT_QUEUE_URL", "https://sqs.us-east-2.amazonaws.com/211125768252/Dev-Transcript"
    )
    WORKERS = os.environ.get("WORKERS", 50)

    record = event["Records"][0]

    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    response = s3_client.get_object(Bucket=bucket, Key=key)
    body = json.loads(response["Body"].read())

    video_id = body["jobName"]
    transcription = body["results"]["items"]

    total_items = len(transcription)
    items_per_batch = math.ceil(total_items / WORKERS)
    batches = [transcription[i : i + items_per_batch] for i in range(0, total_items, items_per_batch)]

    for batch in batches:
        sqs.send_message(
            QueueUrl=TRANSCRIPT_QUEUE_URL, MessageBody=json.dumps({"video_id": video_id, "transcription": batch})
        )


event = {
    "Records": [
        {
            "s3": {
                "bucket": {"name": "live-cut-the-bullshit-transcriptions"},
                "object": {"key": "5548f4c0-f5bb-49c9-a026-0f65ef10c412.json"},
            }
        }
    ]
}
lambda_handler(event, {})

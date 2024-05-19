import json
import os
import boto3
from datetime import datetime, timedelta, timezone


def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")

    body = json.loads(event["Records"][0]["body"])
    video_id = body["video_id"]
    transcription = body["transcription"]

    VIDEOS_TABLE_NAME = os.environ.get("VIDEOS_TABLE_NAME", "Dev-Videos")
    TRANSCRIPTIONS_TABLE_NAME = os.environ.get("TRANSCRIPTIONS_TABLE_NAME", "Dev-Transcriptions")

    videos_table = dynamodb.Table(VIDEOS_TABLE_NAME)
    transcriptions_table = dynamodb.Table(TRANSCRIPTIONS_TABLE_NAME)

    video = videos_table.get_item(Key={"PK": video_id})["Item"]

    start_date = datetime.fromisoformat(video["start_date"])
    seconds = 0
    for word in transcription:
        content = word["alternatives"][0]["content"]
        
        if word["type"] == "pronunciation":
            seconds += float(word["end_time"]) - float(word["start_time"])
            
        elif word["type"] == "punctuation":
            seconds += 0.1

        timestamp = start_date + timedelta(seconds=seconds)
        transcriptions_table.put_item(Item={"PK": video_id, "SK": timestamp.isoformat(), "content": content})

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

    video_start_date = datetime.fromisoformat(video["start_date"])
    transcription_start_date_in_seconds = float(transcription[0]["start_time"])
    transcription_end_date_in_seconds = float(transcription[-1]["end_time"])

    transcription_start_timestamp = video_start_date + timedelta(seconds=transcription_start_date_in_seconds)
    transcription_end_timestamp = video_start_date + timedelta(seconds=transcription_end_date_in_seconds)

    content = ""
    for word in transcription:
        content += word["alternatives"][0]["content"] + " "

    transcriptions_table.put_item(
        Item={
            "PK": video_id,
            "SK": transcription_start_timestamp.isoformat(),
            "end_transcription": transcription_end_timestamp.isofomat(),
            "transcription": content,
        }
    )



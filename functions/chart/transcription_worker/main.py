import json
import os
from datetime import datetime, timedelta, timezone

import boto3


def get_last_valid_end_time(transcription, key):
    for item in transcription:
        if "end_time" in item:
            try:
                end_time = float(item[key])
                return end_time
            except ValueError:
                continue
    return None


def lambda_handler(event, context):

    dynamodb = boto3.resource("dynamodb")

    body = json.loads(event["Records"][0]["body"])
    video_id = body["video_id"]
    transcription = body["transcription"]
    interval = body["interval"]

    VIDEOS_TABLE_NAME = os.environ.get("VIDEOS_TABLE_NAME", "Dev-Videos")
    TRANSCRIPTIONS_TABLE_NAME = os.environ.get("TRANSCRIPTIONS_TABLE_NAME", "Dev-Transcriptions")

    videos_table = dynamodb.Table(VIDEOS_TABLE_NAME)
    transcriptions_table = dynamodb.Table(TRANSCRIPTIONS_TABLE_NAME)

    video = videos_table.get_item(Key={"PK": video_id})["Item"]

    video_start_date = datetime.fromisoformat(video["start_date"])
    transcription_start_date_in_seconds = get_last_valid_end_time(transcription, "start_time")
    transcription_end_date_in_seconds = get_last_valid_end_time(reversed(transcription), "end_time")

    transcription_start_timestamp = video_start_date + timedelta(seconds=transcription_start_date_in_seconds)
    transcription_end_timestamp = video_start_date + timedelta(seconds=transcription_end_date_in_seconds)

    content = ""
    for word in transcription:
        if word["type"] == "pronunciation":
            content += " " + word["alternatives"][0]["content"]

        else:
            content += word["alternatives"][0]["content"]

    transcriptions_table.put_item(
        Item={
            "PK": f"{video_id}#INTERVAL={interval}",
            "SK": transcription_start_timestamp.isoformat(),
            "end_transcription": transcription_end_timestamp.isoformat(),
            "transcription": content.strip(),
        }
    )


# batches = json.load(open("batches.json"))
# for batch in batches:
#     lambda_handler({"Records": [{"body": json.dumps({**batch, "interval": 10})}]}, None)

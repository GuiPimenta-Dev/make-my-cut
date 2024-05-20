import datetime
import json
import os
from datetime import timezone
from io import BytesIO

import boto3
from pytube import YouTube
from googleapiclient.discovery import build


def lambda_handler(event, context):

    VIDEOS_BUCKET_NAME = os.environ.get("VIDEOS_BUCKET_NAME", "live-cut-the-bullshit-videos")
    VIDEOS_TABLE_NAME = os.environ.get("VIDEOS_TABLE_NAME", "Dev-Videos")
    VIDEOS_TOPIC_ARN = os.environ.get(
        "VIDEOS_TOPIC_ARN", "arn:aws:sns:us-east-2:211125768252:Live-Cut-The-Bullshit-Videos"
    )

    body = json.loads(event["Records"][0]["body"])
    url = body["url"]
    video_id = body["video_id"]
    language = body["language"]

    buffer = BytesIO()

    yt = YouTube(url)
    video_stream = yt.streams.filter(file_extension="mp4").first()
    video_stream.stream_to_buffer(buffer)
    buffer.seek(0)

    s3_client = boto3.client("s3")
    s3_client.put_object(
        Bucket=VIDEOS_BUCKET_NAME,
        Key=f"{video_id}.mp3",
        Body=buffer,
        Metadata={"url": url, "video_id": video_id},
    )

    duration_in_seconds = yt.length
    hours, remainder = divmod(duration_in_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_formatted = f"{hours:02}:{minutes:02}:{seconds:02}"

    dynamodb = boto3.resource("dynamodb")
    videos_table = dynamodb.Table(VIDEOS_TABLE_NAME)

    videos_table.put_item(
        Item={
            "PK": video_id,
            "url": url,
            "title": yt.title,
            "language": language,
            "publish_date": yt.publish_date.isoformat(),
            "duration": duration_formatted,
        }
    )

    sns_client = boto3.client("sns")
    sns_client.publish(
        TopicArn=VIDEOS_TOPIC_ARN,
        Message=json.dumps({"video_id": video_id, "url": url}),
    )


event = {
    "Records": [
        {"body": '{"url": "https://www.youtube.com/watch?v=EYFpRvwK5sE", "video_id": "Q5okdHvzjK8", "language": "en"}'}
    ]
}
lambda_handler(event, None)

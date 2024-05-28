import json
import os

import boto3


def lambda_handler(event, context):

    TRANSCRIPTIONS_BUCKET_NAME = os.environ.get("TRANSCRIPTIONS_BUCKET_NAME", "live-cut-the-bullshit-transcriptions")
    VIDEOS_TABLE_NAME = os.environ.get("VIDEOS_TABLE_NAME", "Dev-Videos")

    s3_client = boto3.client("s3")
    transcribe_client = boto3.client("transcribe")
    dynamodb = boto3.resource("dynamodb")

    record = event["Records"][0]
    message = json.loads(record["Sns"]["Message"])

    video_id = message["video_id"]

    bucket_name = "live-cut-the-bullshit-videos"
    object_key = f"{video_id}.mp3"
    
    s3_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)

    video_id = s3_object["Metadata"]["video_id"]
    job_uri = f"s3://{bucket_name}/{object_key}"

    videos_table = dynamodb.Table(VIDEOS_TABLE_NAME)
    video = videos_table.get_item(Key={"PK": video_id})["Item"]

    transcribe_client.start_transcription_job(
        TranscriptionJobName=video_id,
        Media={"MediaFileUri": job_uri},
        MediaFormat="mp3",
        LanguageCode=video["language"],
        OutputBucketName=TRANSCRIPTIONS_BUCKET_NAME,
    )


import datetime
import json
import os

import boto3
from chat_downloader import ChatDownloader as cd


def lambda_handler(event, context):
  
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

    CHAT_TABLE_NAME = os.environ.get("CHAT_TABLE_NAME", "Dev-Live-Chat")
    chats_table = dynamodb.Table(CHAT_TABLE_NAME)

    record = event["Records"][0]
    message = json.loads(record["Sns"]["Message"])

    video_id = message["video_id"]
    url = message["url"]

    chat = cd().get_chat(url)

    for message in chat:
        timestamp_seconds = message["timestamp"] / 1_000_000
        utc_datetime = datetime.datetime.utcfromtimestamp(timestamp_seconds)

        # Attach the UTC timezone
        utc_datetime = utc_datetime.replace(tzinfo=datetime.timezone.utc)

        # Format the datetime string to include the timezone information
        formatted_date = utc_datetime.strftime("%Y-%m-%d %H:%M:%S %Z%z")

        chats_table.put_item(
            Item={
                "PK": video_id,
                "SK": formatted_date,
                "message": message["message"],
                "author": message["author"],
            }
        )


event = {
  "Records": [
    {
      "EventSource": "aws:sns",
      "EventVersion": "1.0",
      "EventSubscriptionArn": "arn:aws:sns:us-east-1:211125768252:Live-Make-My-Cut-videos_topic:b60d27fa-c2c0-4d88-822c-725c88cecc86",
      "Sns": {
        "Type": "Notification",
        "MessageId": "11e346e2-2080-5d15-a903-18277d5c6b5b",
        "TopicArn": "arn:aws:sns:us-east-1:211125768252:Live-Make-My-Cut-videos_topic",
        "Subject": None,
        "Message": "{\"video_id\": \"847e4153-4fde-40bf-8ed1-cb26d51d0a16\", \"url\": \"https://www.youtube.com/watch?v=GSrC2HISJVc\"}",
        "Timestamp": "2024-05-20T14:18:04.183Z",
        "SignatureVersion": "1",
        "Signature": "NmCcRg2grT6jEypgh3dvj1FuNlqCpBhoHEiiiImQ98SB53b7tw/t4/8E3J4KfGUT2ABbZabkAycYk2II8dvkNfwoARr6Ib0rgdzwkb4cFyEHF4FVrjZ6eEVWxYuZIiK6pdWDqFMIHFtrQLapuIVfQ1HvNihjHK4jlNlJbB0VON1yueDwyIU4O0Gr1kQr/O0qcfkOnBZOo7veo2LzHtWieHr8e7zspETraFOxW13nQcwhV/frO30XEghd9gzliFbyvQ4trSroXW6IlEmrlR00lksUh4vfCLgxgInx3GwPgvEcCO04RLwAhpDsoj6w78+mzAWt2FeH8YU12S2I20HHMA==",
        "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-60eadc530605d63b8e62a523676ef735.pem",
        "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:211125768252:Live-Make-My-Cut-videos_topic:b60d27fa-c2c0-4d88-822c-725c88cecc86",
        "MessageAttributes": {}
      }
    }
  ]
}
lambda_handler(event, {})

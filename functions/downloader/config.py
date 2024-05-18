from infra.services import Services


class DownloaderConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Downloader",
            path="./functions/downloader",
            description="Download a YouTube video and Stores it on S3",
            layers=[services.layers.pytube_layer],
            memory_size=512,
            timeout=15,
            environment={
                "VIDEOS_BUCKET_NAME": services.s3.videos_bucket.bucket_name,
                "VIDEOS_TABLE_NAME": services.dynamo_db.videos_table.table_name,
                "VIDEOS_TOPIC_ARN": services.sns.videos_topic.topic_arn,
            },
        )

        services.sqs.create_trigger(services.sqs.downloads_queue, function)

        services.sqs.downloads_queue.grant_consume_messages(function)

        services.s3.videos_bucket.grant_read_write(function)

        services.dynamo_db.videos_table.grant_write_data(function)

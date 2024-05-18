from infra.services import Services


class TranscribeConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Transcribe",
            path="./functions/transcribe",
            description="Transcript audio to text",
            environment={
                "TRANSCRIPTIONS_BUCKET_NAME": services.s3.transcriptions_bucket.bucket_name,
                "VIDEOS_TABLE_NAME": services.dynamo_db.videos_table.table_name,
            },
        )

        services.s3.create_trigger(bucket=services.s3.transcriptions_bucket, function=function)

        services.s3.transcriptions_bucket.grant_read_write(function)
        
        services.dynamo_db.videos_table.grant_read_data(function)

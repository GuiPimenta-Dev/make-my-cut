from infra.services import Services


class TranscriptionWorkerConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="TranscriptionWorker",
            path="./functions/chart",
            description="Parse the transcription",
            directory="transcription_worker",
            environment={
                "VIDEOS_TABLE_NAME": services.dynamo_db.videos_table.table_name,
                "TRANSCRIPTIONS_TABLE_NAME": services.dynamo_db.transcriptions_table.table_name,
            },
        )

        services.sqs.add_event_source("transcript_queue", function)

        services.dynamo_db.grant_write_data("transcriptions_table", function)

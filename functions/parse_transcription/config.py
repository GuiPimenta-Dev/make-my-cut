from infra.services import Services


class ParseTranscriptionConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="ParseTranscription",
            path="./functions/parse_transcription",
            description="Parse the transcription",
            environment={
                "TRANSCRIPTIONS_QUEUE_URL": services.sqs.transcript_queue.queue_url,
                "WORKERS": 15,
            },
        )

        services.s3.add_event_notification("transcriptions_bucket", function)

        services.sqs.grant_send_messages("transcript_queue", function)

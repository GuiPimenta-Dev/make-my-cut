from aws_cdk import Duration
from aws_cdk import aws_sqs as sqs
from aws_cdk.aws_lambda_event_sources import SqsEventSource


class SQS:
    def __init__(self, scope, context) -> None:

        self.downloads_queue = sqs.Queue(
            scope,
            "DownloadsQueue",
            queue_name=f"{context.stage.lower()}-downloads",
            visibility_timeout=Duration.minutes(1),
        )

        self.compreensions_queue = sqs.Queue(
            scope,
            "CompreensionsQueue",
            queue_name=f"{context.stage.lower()}-compreensions",
            visibility_timeout=Duration.minutes(15),
        )

    @staticmethod
    def create_trigger(queue, function):
        function.add_event_source(SqsEventSource(queue))

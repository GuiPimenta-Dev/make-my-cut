from aws_cdk import Duration
from aws_cdk import aws_sqs as sqs
from aws_cdk import aws_lambda_event_sources
from lambda_forge.trackers import trigger, invoke

class SQS:
    def __init__(self, scope, context) -> None:

        self.downloads_queue = sqs.Queue(
            scope,
            "DownloadsQueue",
            queue_name=f"{context.stage.lower()}-downloads",
            visibility_timeout=Duration.minutes(15),
        )

        self.compreensions_queue = sqs.Queue(
            scope,
            "CompreensionsQueue",
            queue_name=f"{context.stage.lower()}-compreensions",
            visibility_timeout=Duration.minutes(15),
        )

    @trigger(service="sqs", trigger="queue", function="function")
    def add_event_source(self, queue, function):
        queue = getattr(self, queue)
        event_source = aws_lambda_event_sources.SqsEventSource(queue)
        function.add_event_source(event_source)
        queue.grant_consume_messages(function)


    @invoke(service="sqs", resource="queue", function="function")
    def grant_send_messages(self, queue, function):
        queue = getattr(self, queue)
        queue.grant_send_messages(function)
from aws_cdk.aws_sns import Topic
from aws_cdk import aws_lambda_event_sources


class SNS:
    def __init__(self, scope, context) -> None:
        
        self.videos_topic = Topic.from_topic_arn(
            scope,
            "VideosTopic",
            topic_arn=context.resources["arns"]["videos_topic_arn"],
        )

    def create_trigger(self, topic, function, stages=None):
        if stages and self.stage not in stages:
            return

        sns_subscription = aws_lambda_event_sources.SnsEventSource(topic)
        function.add_event_source(sns_subscription)
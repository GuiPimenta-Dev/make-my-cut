from aws_cdk import aws_dynamodb as dynamo_db
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_lambda_event_sources as event_source
from lambda_forge.trackers import invoke, trigger


class DynamoDB:
    def __init__(self, scope, context) -> None:

        self.videos_table = dynamo_db.Table.from_table_arn(
            scope,
            "VideosTable",
            context.resources["arns"]["videos_table_arn"],
        )

        self.chats_table = dynamo_db.Table.from_table_arn(
            scope,
            "ChatsTable",
            context.resources["arns"]["chats_table_arn"],
        )

        self.transcriptions_table = dynamo_db.Table(
            scope,
            "TranscriptionsTable",
            table_name=f"{context.stage}-{context.name}-Transcriptions",
            partition_key=dynamo_db.Attribute(name="PK", type=dynamo_db.AttributeType.STRING),
            sort_key=dynamo_db.Attribute(name="SK", type=dynamo_db.AttributeType.STRING),
            stream=dynamo_db.StreamViewType.NEW_AND_OLD_IMAGES,
        )

    @trigger(service="dynamodb", trigger="table", function="function")
    def create_stream(self, table, function):
        table = getattr(self, table)
        my_dynamo_event_stream = event_source.DynamoEventSource(
            table, starting_position=lambda_.StartingPosition.TRIM_HORIZON
        )
        function.add_event_source(my_dynamo_event_stream)

    @invoke(service="dynamodb", resource="table", function="function")
    def grant_write_data(self, table, function):
        table = getattr(self, table)
        table.grant_write_data(function)

    @staticmethod
    def add_query_permission(table, function):
        function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:Query"],
                resources=[f"{table.table_arn}/index/*"],
            )
        )

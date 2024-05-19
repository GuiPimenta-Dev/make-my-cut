from aws_cdk import aws_dynamodb as dynamo_db
from aws_cdk import aws_iam as iam
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

        self.transcriptions_table = dynamo_db.Table.from_table_arn(
            scope,
            "TranscriptionsTable",
            context.resources["arns"]["transcriptions_table_arn"],
        )

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

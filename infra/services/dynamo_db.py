from aws_cdk import aws_dynamodb as dynamo_db
from aws_cdk import aws_iam as iam
from lambda_forge.trackers import invoke


class DynamoDB:
    def __init__(self, scope, context) -> None:

        self.compreensions_table = dynamo_db.Table.from_table_arn(
            scope,
            "CompreensionsTable",
            context.resources["arns"]["compreensions_table_arn"],
        )

        self.videos_table = dynamo_db.Table.from_table_arn(
            scope,
            "VideosTable",
            context.resources["arns"]["videos_table_arn"],
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

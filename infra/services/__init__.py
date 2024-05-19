from infra.services.api_gateway import APIGateway
from infra.services.aws_lambda import Lambda
from infra.services.dynamo_db import DynamoDB
from infra.services.layers import Layers
from infra.services.s3 import S3
from infra.services.sns import SNS
from infra.services.sqs import SQS


class Services:
    def __init__(self, scope, context) -> None:
        self.api_gateway = APIGateway(scope, context)
        self.aws_lambda = Lambda(scope, context)
        self.layers = Layers(scope)
        self.s3 = S3(scope, context)
        self.sqs = SQS(scope, context)
        self.dynamo_db = DynamoDB(scope, context)
        self.sns = SNS(scope, context)

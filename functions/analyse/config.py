from infra.services import Services


class AnalyseConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Analyse", path="./functions/analyse", description="Makes the analysis"
        )

        services.api_gateway.create_endpoint("GET", "/analyse", function, public=True)

        services.dynamo_db.chats_table.grant_read_data(function)

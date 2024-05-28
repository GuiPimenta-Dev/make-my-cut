from infra.services import Services

class GetChartConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="GetChart",
            path="./functions/chart",
            description="Rate interactions based on transcription and chat",
            directory="get_chart"
        )

        services.api_gateway.create_endpoint("GET", "/chart", function, public=True)
        
        services.dynamo_db.transcriptions_table.grant_read_data(function)
        
        services.dynamo_db.add_query_permission(services.dynamo_db.transcriptions_table, function)
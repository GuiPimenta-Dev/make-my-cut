from infra.services import Services


class GetChartConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="GetChart", path="./functions/chart", description="Parse the transcription", directory="get_chart"
        )

        services.api_gateway.create_endpoint("GET", "/chart", function, public=True)

        services.sqs.grant_send_messages("transcript_queue", function)

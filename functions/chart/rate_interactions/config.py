from infra.services import Services


class RateInteractionsConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="RateInteractions",
            path="./functions/chart",
            description="Rate interactions based on transcription and chat",
            directory="rate_interactions",
        )

        services.dynamo_db.create_stream("transcriptions_table", function)

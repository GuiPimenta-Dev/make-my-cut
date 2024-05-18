from infra.services import Services


class GetChatConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="GetChat",
            path="./functions/get_chat",
            description="Get Live chat messages and stores on DynamoDB",
            timeout=15,
            memory_size=512,
            layers=[services.layers.chat_downloader_layer],
            environment={
                "COMPREENSIONS_QUEUE_URL": services.sqs.compreensions_queue.queue_url,
            },
        )

        services.sns.create_trigger(services.sns.videos_topic, function)

        services.s3.videos_bucket.grant_read_write(function)

        services.sqs.compreensions_queue.grant_send_messages(function)

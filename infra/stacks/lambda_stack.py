from aws_cdk import Stack
from constructs import Construct
from lambda_forge.trackers import reset

from functions.chart.get_chart.config import GetChartConfig
from functions.chart.transcription_worker.config import \
    TranscriptionWorkerConfig
from functions.downloader.config import DownloaderConfig
from functions.get_chat.config import GetChatConfig
from functions.starter.config import StarterConfig
from functions.transcribe.config import TranscribeConfig
from infra.services import Services


@reset
class LambdaStack(Stack):
    def __init__(self, scope: Construct, context, **kwargs) -> None:

        super().__init__(scope, f"{context.name}-Lambda-Stack", **kwargs)

        self.services = Services(self, context)

        # Downloader
        DownloaderConfig(self.services)

        # Starter
        StarterConfig(self.services)

        # GetChat
        GetChatConfig(self.services)

        # Transcribe
        TranscribeConfig(self.services)

        # Chart
        GetChartConfig(self.services)
        TranscriptionWorkerConfig(self.services)

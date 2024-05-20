from functions.chart.get_chart.config import GetChartConfig
from aws_cdk import Stack
from constructs import Construct
from lambda_forge.trackers import reset

from functions.chart.create_chart.config import CreateChartConfig
from functions.chart.transcription_worker.config import TranscriptionWorkerConfig
from functions.download.downloader.config import DownloaderConfig
from functions.download.get_chat.config import GetChatConfig
from functions.download.starter.config import StartDownloadConfig
from functions.download.transcribe.config import TranscribeConfig
from infra.services import Services


@reset
class LambdaStack(Stack):
    def __init__(self, scope: Construct, context, **kwargs) -> None:

        super().__init__(scope, f"{context.name}-Lambda-Stack", **kwargs)

        self.services = Services(self, context)

        # Download
        StartDownloadConfig(self.services)
        DownloaderConfig(self.services)
        GetChatConfig(self.services)
        TranscribeConfig(self.services)

        # Chart
        GetChartConfig(self.services)
        CreateChartConfig(self.services)
        TranscriptionWorkerConfig(self.services)

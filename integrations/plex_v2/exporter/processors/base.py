from baseintegration.exporter.processor import BaseProcessor
from baseintegration.integration.integration_export_report import IntegrationExportReport
from plex_v2.configuration import PlexConfig


class PlexProcessor(BaseProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME: str = None
    integration_report: IntegrationExportReport
    config: PlexConfig

    def __init__(self, exporter):
        """
        We want to ensure that each time a Processor is created, it has a reference to the Integration that created it
        to access context and configuration data.
        """
        self._exporter = exporter
        self.integration_report = self._exporter.integration_report
        self.config = exporter.erp_config

    def _add_report_message(self, message: str):
        # ensure the processor has an integration report column defined
        if self.INTEGRATION_EXPORT_REPORT_COLUMN_NAME is None:
            raise Exception(f'{self.__class__.__name__} does not have an integration report column defined')

        self.integration_report.add_message(self.INTEGRATION_EXPORT_REPORT_COLUMN_NAME, message)

from baseintegration.importer.import_processor import BaseImportProcessor
from plex_v2.configuration import PlexConfig
from baseintegration.importer import BaseImporter


class PlexImportProcessor(BaseImportProcessor):

    config: PlexConfig

    def __init__(self, importer: BaseImporter):
        """
        We want to ensure that each time a Processor is created, it has a reference to the Integration that created it
        to access context and configuration data.
        """
        self.config = importer.erp_config
        self._importer = importer

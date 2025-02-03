
from typing import List
from dataclasses import dataclass
from baseintegration.datamigration import logger
from datetime import datetime, timedelta


@dataclass
class PlexRepeatWorkImportListener:

    def __init__(self, integration):
        self.identifier = "import_repeat_part"
        self._integration = integration
        logger.info("Plex repeat work import listener was instantiated")

    def get_new(self, bulk=False) -> List[str]:
        # 1) establish date to search
        date_to_search = self._integration.config_yaml.get("Importers", {}).get("repeat_part", {}).get(
            "import_objects_newer_than", datetime.now() - timedelta(days=5 * 365))

        logger.info(f'Date to search: {date_to_search}')

        # somehow need to get updated quotes then go from there
        # we can get updated orders using the sales orders endpoint (kind of, i dont think we can actually only pull whats updated)
        # now we need to go from order to quote

        return []

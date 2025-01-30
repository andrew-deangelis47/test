from integrations.baseintegration.utils import get_last_action_datetime
from typing import List
from sage.sage_api.client import SageImportClient
from sage.models.sage_models.work_center.work_center_full_entity import WorkCenterFullEntity
from sage.sage_api.filter_generation.work_center_filter_generator import WorkCenterFilterGenerator


class SageWorkCenterImportListener:
    identifier: str = "import_work_center"

    def __init__(self, integration):
        self.identifier = "import_work_center"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Listens for changes to part numbers of config-specified ClassIDs based on ChangedOn dates
        - Returns string type part numbers in a list.
        """

        # 1) get last run time
        last_action_date = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                    bulk=bulk)

        # 2) make the call to Sage api
        client = SageImportClient.get_instance()
        work_centers = client.get_resource(
            WorkCenterFullEntity,
            WorkCenterFilterGenerator.get_filter_by_last_update_time(last_action_date)
        )

        # 4) massage data
        work_center_ids = []
        for work_center in work_centers:
            work_center_ids.append(work_center.work_center.work_center_id)

        return work_center_ids

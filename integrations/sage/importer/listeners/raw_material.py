from integrations.baseintegration.utils import get_last_action_datetime
from typing import List
from sage.sage_api.client import SageImportClient
from sage.models.sage_models.part import PartFullEntity
from sage.sage_api.filter_generation.part_filter_generator import PartFilterGenerator


class SageRawMaterialImportListener:
    identifier: str = "import_material"

    def __init__(self, integration):
        self.identifier = "import_material"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Listens for changes to part numbers of config-specified ClassIDs based on ChangedOn dates
        - Returns string type part numbers in a list.
        """

        # 1) Get class for raw material, needed for api filter
        raw_material_class = self._integration.config_yaml["Importers"]["materials"].get("material_code", [])

        # 2) get last run time
        last_action_date = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                    bulk=bulk)

        # 3) make the call to Sage api
        client = SageImportClient.get_instance()
        raw_materials = client.get_resource(
            PartFullEntity,
            PartFilterGenerator.get_filter_by_last_update_time(last_action_date, raw_material_class)
        )

        # 4) make a list of material ids
        raw_material_ids = []
        for raw_material in raw_materials:
            raw_material_ids.append(raw_material.product.product_code)

        return raw_material_ids

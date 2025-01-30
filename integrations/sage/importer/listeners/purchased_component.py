from typing import List
from sage.sage_api.client import SageImportClient
from integrations.baseintegration.utils import get_last_action_datetime
from sage.models.sage_models.part import PartFullEntity
from sage.sage_api.filter_generation.part_filter_generator import PartFilterGenerator


class SagePurchasedComponentsImportListener:
    identifier: str = "import_purchased_component"

    def __init__(self, integration):
        self.identifier = "import_purchased_component"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Listens for changes to part numbers of config-specified ClassIDs based on ChangedOn dates
        - Returns string type part numbers in a list.
        """

        # 1) get material class, used for api filter
        purchased_components_class = self._integration.config_yaml["Importers"]["purchased_components"].get("material_code", [])

        # 2) get last run time
        last_action_date = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                    bulk=bulk)

        # 3) make the call to Sage api
        client = SageImportClient.get_instance()
        purchased_components = client.get_resource(
            PartFullEntity,
            PartFilterGenerator.get_filter_by_last_update_time(last_action_date, purchased_components_class)
        )

        # 4) make a list of component ids
        purchased_components_ids = []
        for purchased_component in purchased_components:
            purchased_components_ids.append(purchased_component.product.product_code)

        return purchased_components_ids

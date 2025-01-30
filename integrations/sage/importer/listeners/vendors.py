from integrations.baseintegration.utils import get_last_action_datetime
from typing import List
from sage.sage_api.client import SageImportClient
from sage.sage_api.filter_generation.vendor_filter_generator import VendorFilterGenerator
from sage.models.sage_models.vendor import SupplierFullEntity


class SageVendorImportListener:
    identifier: str = "import_vendor"

    def __init__(self, integration):
        self.identifier = "import_vendor"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Listens for changes to part numbers of config-specified ClassIDs based on ChangedOn dates
        - Returns string type part numbers in a list.
        """

        # 1) get last run time
        last_action_date = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                    bulk=bulk)

        # 3) make the call to Sage api
        client = SageImportClient.get_instance()
        suppliers = client.get_resource(
            SupplierFullEntity,
            VendorFilterGenerator.get_filter_by_last_update_time(last_action_date)
        )

        # 4) make a list of vendor ids
        vendor_ids = []
        for supplier in suppliers:
            vendor_ids.append(supplier.supplier.vendor_id)

        return vendor_ids

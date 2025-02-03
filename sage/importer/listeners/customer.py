from typing import List
from sage.sage_api.client import SageImportClient
from integrations.baseintegration.utils import get_last_action_datetime
from sage.models.sage_models.customer.customer_full_entity import SageCustomerFullEntity
from sage.sage_api.filter_generation.customer_filter_generator import CustomerFilterGenerator


class SageCustomerImportListener:
    identifier: str = "import_customer"

    def __init__(self, integration):
        self.identifier = "import_customer"
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
        sage_customers = client.get_resource(
            SageCustomerFullEntity,
            CustomerFilterGenerator.get_filter_by_last_update_time(last_action_date)
        )

        # 3) make a list of customer ids
        customer_ids = []
        for sage_customer in sage_customers:
            customer_ids.append(sage_customer.customer.code)

        return customer_ids

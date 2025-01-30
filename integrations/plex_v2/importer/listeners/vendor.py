from plex_v2.objects.supplier import Supplier
from baseintegration.utils import get_last_action_datetime
from pendulum.datetime import DateTime
from datetime import datetime
from typing import List


class PLEXVendorListener:
    identifier = "work_center_import"

    def __init__(self, integration, erp_config):
        self._integration = integration
        self._erp_config = erp_config

    def get_new(self, bulk=False):
        """
        This actually listens for supplier updates
        """

        now: str = datetime.now().isoformat()
        last_action_date: DateTime = get_last_action_datetime(self._integration.managed_integration_uuid,
                                                              self.identifier,
                                                              bulk=bulk)

        return self._get_filtered_supplier_codes(now, last_action_date)

    def _get_filtered_supplier_codes(self, now_time: str, last_action_date: DateTime) -> List[str]:
        """
        filters suppliers based on config
        1) supplier types
        2) import only active suppliers
        """

        updated_supplier_ids = []
        for supplier_type in self._erp_config.supplier_types:
            suppliers_for_type = Supplier.search(type=supplier_type)

            # only add if it's a new update
            for supplier in suppliers_for_type:
                if self._was_updated_since_last_run(supplier, last_action_date, now_time):
                    # only import not blacklisted statuses
                    if supplier.status not in self._erp_config.supplier_status_blacklist:
                        updated_supplier_ids.append(supplier.code)

        return updated_supplier_ids

    def _was_updated_since_last_run(self, supplier: Supplier, last_action_date: DateTime, now: str) -> bool:
        material_update_date: str = now
        if supplier.modifiedDate is not None and supplier.modifiedDate != '':
            material_update_date = supplier.modifiedDate
        elif supplier.createdDate is not None and supplier.createdDate != '':
            material_update_date = supplier.createdDate

        dot_location = len(material_update_date)
        try:
            dot_location = material_update_date.index('.')
        except ValueError:
            pass
        material_update_date = material_update_date[:dot_location]
        modified_date = datetime.fromisoformat(material_update_date.replace('Z', ''))  # Zulu Timestamp conversion

        return modified_date > last_action_date

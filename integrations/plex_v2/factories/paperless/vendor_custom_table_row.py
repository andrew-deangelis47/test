from plex_v2.configuration import PlexConfig
from plex_v2.objects.supplier import Supplier
from pytz import timezone
from pendulum.datetime import DateTime


class VendorCustomTableRowFactory:

    def __init__(self, erp_config: PlexConfig):
        self.erp_config = erp_config

    def to_custom_table_row(self, supplier: Supplier):
        return {
            "Supplier_Code": supplier.code,
            "Supplier_Name": supplier.name,
            "Category": supplier.category,
            "Type": supplier.type,
            "Status": supplier.status,
            "Last_Import_Time": self._get_current_time()
        }

    def _get_current_time(self) -> str:
        tz = timezone('EST5EDT')
        return (str(DateTime.now(tz))[0:19]).replace('T', ' ')

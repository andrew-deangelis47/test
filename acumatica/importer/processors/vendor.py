from paperless.client import PaperlessClient

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import custom_table_patch

from acumatica.api_models.acumatica_models import Vendor
from acumatica.api_models.paperless_custom_tables import VendorCustomTableFormat


class AcumaticaVendorImportProcessor(BaseImportProcessor):

    def format_as_row(self, vendor: Vendor):
        data = dict(vendor_id=vendor.VendorID,
                    name=vendor.VendorName,
                    vendor_class=vendor.VendorClass)
        return data

    def _process(self, vendor_id: str) -> bool:
        logger.info(f'Processing vendor {vendor_id}')
        vendor: Vendor = Vendor.get_by_id(id=vendor_id)
        logger.info(vendor)
        table_model = VendorCustomTableFormat
        vendor_row = self.format_as_row(vendor=vendor)
        logger.info(vendor_row)
        # TODO parent class should probably just do this
        id_name: str = table_model._primary_key
        table_name: str = self._importer.table_name
        url = f"suppliers/public/custom_tables/{table_name}/row"
        paperless_client: PaperlessClient = PaperlessClient.get_instance()
        custom_table_patch(client=paperless_client, data=dict(row_data=vendor_row), url=url, identifier=id_name)
        return True

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import custom_table_patch
from baseintegration.utils.custom_table import ImportCustomTable
from paperless.client import PaperlessClient
from vendor import Vendor, VendorRecord


class VendorImportProcessor(BaseImportProcessor):

    def _process(self, vendor_id: str):
        logger.info("Calling vendor process method")
        vendor_dict = self.get_vendor(vendor_id, self._importer.header_dict.copy())
        if vendor_dict:
            headers = ImportCustomTable.assemble_custom_headers(vendor_dict)
            new_record = ImportCustomTable.generate_custom_header_nr(vendor_dict, headers)
            data = dict(row_data=new_record)
            client = PaperlessClient.get_instance()
            url = "suppliers/public/custom_tables/gss_vendors/row"
            custom_table_patch(client=client, data=data, url=url, identifier=vendor_id)

    def get_vendor(self, vendor_id: str, base_dict: dict) -> dict:
        vendor: VendorRecord = Vendor.get(vendor_id=vendor_id)
        logger.info(f"Vendor is : {vendor}")

        base_dict["vendor"] = vendor.vendor
        base_dict["name_vendor"] = vendor.name_vendor
        return base_dict

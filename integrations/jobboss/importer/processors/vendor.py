from baseintegration.importer.import_processor import BaseImportProcessor
from jobboss.models import Vendor
from baseintegration.utils.custom_table import ImportCustomTable
from paperless.client import PaperlessClient
from baseintegration.utils import custom_table_patch


class VendorImportProcessor(BaseImportProcessor):

    def _process(self, vendor_id: str):  # noqa: C901
        base_dict = self._importer.header_dict.copy()
        vendor_instance = Vendor.objects.filter(vendor=vendor_id).first()
        if not vendor_instance:
            raise Exception(f"Was not able to import {vendor_instance} as it could not be found in the Vendor table")
        if vendor_instance is not None and self.vendor_is_active(vendor_instance):
            dict_to_upload = self.get_vendor(vendor_instance, base_dict)
            if dict_to_upload:
                headers = ImportCustomTable.assemble_custom_headers(dict_to_upload)
                new_record = ImportCustomTable.generate_custom_header_nr(dict_to_upload, headers)
                data = dict(row_data=new_record)
                client = PaperlessClient.get_instance()
                url = f"suppliers/public/custom_tables/{self._importer.table_name}/row"
                custom_table_patch(client=client, data=data, url=url, identifier=vendor_id)

    def get_vendor(self, vendor_instance: Vendor, base_dict: dict):  # noqa: C901
        base_dict["jb_vendor_id"] = vendor_instance.vendor
        base_dict["jb_vendor_name"] = vendor_instance.name
        return base_dict

    @staticmethod
    def vendor_is_active(vendor_instance):
        if vendor_instance is not None and vendor_instance.status == "Active":
            return True
        return False

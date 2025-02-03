from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
from e2.models import Vendcode
from baseintegration.utils.custom_table import ImportCustomTable
from e2.utils import get_version_number


class VendorBulkImportProcessor(BaseImportProcessor):

    def _process(self, vendor_ids: List[str]) -> bool:  # noqa: C901
        vendors: List[dict] = []
        for vendor_id in vendor_ids:
            base_dict = self._importer.header_dict.copy()
            vendor_mst_row = Vendcode.objects.filter(vendcode=vendor_id).first()
            if not vendor_mst_row:
                logger.info(f"Was not able to import {vendor_mst_row} as it could not be found in the vendor table, skipping")
                continue
            dict_to_upload = self.get_vendor(vendor_mst_row, base_dict)
            if dict_to_upload:
                headers = ImportCustomTable.assemble_custom_headers(dict_to_upload)
                new_record = ImportCustomTable.generate_custom_header_nr(dict_to_upload, headers)
                vendors.append(new_record)
        result: dict = ImportCustomTable.upload_records(
            identifier=f'E2-vendor-bulk-upload-count-{len(vendors)}',
            table_name=self._importer.table_name,
            records=vendors)
        return len(result["failures"]) == 0

    def get_vendor(self, vendor_mst_row: Vendcode, base_dict: dict):  # noqa: C901
        base_dict["VendCode"] = vendor_mst_row.vendcode
        base_dict["VendName"] = vendor_mst_row.vendname
        base_dict["VendType"] = vendor_mst_row.vendtype
        base_dict["OutServ"] = vendor_mst_row.outserv
        base_dict["MinOrder"] = vendor_mst_row.minorder
        base_dict["LeadTime"] = vendor_mst_row.leadtime
        if get_version_number() == "default":
            base_dict["LastModDate"] = vendor_mst_row.lastmoddate if vendor_mst_row.lastmoddate is not None else ""
        return base_dict


class VendorImportProcessor(VendorBulkImportProcessor):
    def _process(self, vendor_id: str) -> bool:
        return super()._process([vendor_id])


class VendorBulkPlaceholder:
    pass

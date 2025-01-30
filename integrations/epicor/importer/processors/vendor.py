from copy import deepcopy
from typing import List
from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.custom_table import ImportCustomTable
from epicor.exceptions import EpicorNotFoundException
# Use a module-level variable to make sure this behavior only happens the first time the processor runs (per
# instantiation of the class). This is a way of saving redundant API calls
from epicor.api_models.paperless_custom_tables import VendorCustomTableFormat
from epicor.vendor import Vendor


class EpicorVendorBulkImportProcessor(BaseImportProcessor):

    def _process(self, vendor_ids: List[str]) -> bool:
        vendors: List[dict] = []
        for vendor_id in vendor_ids:
            logger.info(f"Processing vendor {vendor_id}")
            try:
                epicor_vendor: Vendor = Vendor.get_by_id(vendor_id)
            except EpicorNotFoundException:
                logger.info("Vendor not found in Epicor, skipping")
                continue
            if epicor_vendor.Inactive:
                logger.info(f"Vendor {vendor_id} is inactive, moving on")
                continue
            new_table_row: VendorCustomTableFormat = self.set_table_row_attributes(epicor_vendor)
            vendors.append(self.remove_table_name(new_table_row.__dict__))
        table_name: str = "vendors_custom_table"  # TODO: add this to config
        result: dict = ImportCustomTable.upload_records(identifier=f'epicor-vendor-bulk-upload-count-{len(vendors)}',
                                                        table_name=table_name,
                                                        records=vendors)
        return len(result["failures"]) == 0

    def set_table_row_attributes(self, epicor_vendor: Vendor) -> VendorCustomTableFormat:
        paperless_table: VendorCustomTableFormat = deepcopy(self._importer._paperless_table_model)
        paperless_table.vendor_id = epicor_vendor.VendorID
        paperless_table.vendor_num = epicor_vendor.VendorNum
        paperless_table.name = self.get_vendor_name(epicor_vendor)
        # paperless_table.comment = self.get_vendor_comment(epicor_vendor)
        paperless_table.early_buffer = epicor_vendor.EarlyBuffer
        paperless_table.approved = epicor_vendor.Approved
        paperless_table.min_order_value = epicor_vendor.MinOrderValue
        paperless_table.late_buffer = epicor_vendor.LateBuffer
        return paperless_table

    def get_vendor_name(self, epicor_vendor: Vendor) -> str:
        return epicor_vendor.Name

    def get_vendor_comment(self, epicor_vendor: Vendor) -> str:
        return epicor_vendor.Comment

    def remove_table_name(self, table_data: dict):
        try:
            del table_data["_custom_table_name"]
        except Exception:
            return table_data
        return table_data


class EpicorVendorImportProcessor(EpicorVendorBulkImportProcessor):
    def _process(self, vendor_id: str) -> bool:
        return super()._process([vendor_id])


class VendorBulkPlaceholder:
    pass

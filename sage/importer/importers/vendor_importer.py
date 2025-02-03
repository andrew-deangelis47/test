from baseintegration.importer.vendor_importer import VendorImporter
from sage.importer.importer import SageImporter
from sage.models.paperless_custom_tables.vendors_table import VendorsTable
from integrations.baseintegration.utils import Vendor as PaperlessVendor
from sage.importer.listeners.vendors import SageVendorImportListener
from baseintegration.datamigration import logger
from typing import List
from sage.importer.configuration import SageVendorConfig
from sage.importer.processors.vendors import SageBulkVendorImportProcessor, SageVendorImportProcessor, \
    SageVendorBulkPlaceholder


class SageVendorImporter(VendorImporter, SageImporter):
    _paperless_table_model = VendorsTable()

    def _register_listener(self):
        self.listener = SageVendorImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(PaperlessVendor, SageVendorImportProcessor)
        self.register_processor(SageVendorBulkPlaceholder, SageBulkVendorImportProcessor)
        logger.info('Registered vendor processor.')

    def _process_vendor(self, vendor_id: str):  # noqa: C901
        logger.info(f"Vendor id is {str(vendor_id)}")
        with self.process_resource(PaperlessVendor, vendor_id):
            logger.info(f"Processed vendor id: {vendor_id}")

    def _bulk_process_vendors(self, vendors_ids: List[str]):
        with self.process_resource(SageBulkVendorImportProcessor, vendors_ids) as success:
            logger.info(f"Bulk processed {len(vendors_ids)} vendors")
            return success

    def _setup_erp_config(self):
        self.erp_config = SageVendorConfig(self._integration.config_yaml)

    def check_custom_table_exists(self):
        self.add_or_remove_custom_table_attributes()
        self._paperless_table_model.check_custom_header_custom_table_exists()

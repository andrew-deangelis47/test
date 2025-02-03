from baseintegration.datamigration import logger
from baseintegration.importer.vendor_importer import VendorImporter
from plex_v2.configuration import ERPConfigFactory
from plex_v2.importer.listeners import PLEXVendorListener
from plex_v2.importer.processors import VendorImportProcessor, VendorBulkImportProcessor, VendorBulkPlaceholder
from typing import List
from plex_v2.objects.vendor_custom_table import VendorCustomTable
from plex_v2.factories.paperless import VendorCustomTableRowFactory
from integrations.baseintegration.utils import Vendor
import os
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
import yaml
from baseintegration.integration.erp_error_message_converter import ERPErrorMessageConverter


class PLEXVendorImporter(VendorImporter):

    def _setup_erp_config(self):
        # 1) setup config and client
        self.erp_config, self.plex_client = ERPConfigFactory.create_importer_config(self._integration, 'vendors')
        self._paperless_table_model = VendorCustomTable()

        # setup util classes
        self._setup_util_classes()

        # 3) setup factories
        self._setup_factories()

        self._setup_error_message_converter()

    def _setup_factories(self):
        self.vendor_custom_table_row_factory = VendorCustomTableRowFactory(self.erp_config)

    def _setup_util_classes(self):
        """
        util classes not needed but leaving this here for consistency, or if we ever need one in a custom processor
        """
        pass

    def _register_default_processors(self):
        self.register_processor(Vendor, VendorImportProcessor)
        self.register_processor(VendorBulkPlaceholder, VendorBulkImportProcessor)

    def _register_listener(self):
        self.listener = PLEXVendorListener(self._integration, self.erp_config)

    def _process_vendor(self, supplier_id: str):
        logger.info(f"Processing supplier {str(supplier_id)}")
        with self.process_resource(Vendor, supplier_id, self.vendor_custom_table_row_factory) as result:
            return result

    def _bulk_process_vendors(self, supplier_ids: List[str]):  # noqa: C901
        with self.process_resource(VendorBulkImportProcessor, supplier_ids, self.vendor_custom_table_row_factory) as success:
            logger.info(f"Bulk processed {len(supplier_ids)} vendors")
            return success

    def check_custom_table_exists(self):
        self._paperless_table_model.check_custom_header_custom_table_exists()

    def _setup_error_message_converter(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), "../../erp_error_message_mapping.yaml")) as file:
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                config_yaml = yaml.load(file, Loader=yaml.FullLoader)
                self.error_message_converter = ERPErrorMessageConverter(config_yaml.get("Mapping"))
        except Exception as e:
            logger.info(str(e))
            raise CancelledIntegrationActionException('Could not read from error message mapping. Please contact support.')

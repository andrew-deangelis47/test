from baseintegration.datamigration import logger
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from plex_v2.configuration import ERPConfigFactory
from plex_v2.importer.processors.purchased_component import PurchasedComponentImportProcessor, PurchasedComponentBulkImportProcessor, PurchasedComponentBulkPlaceholder
from plex_v2.importer.listeners import PLEXPurchasedComponentListener
from paperless.objects.purchased_components import PurchasedComponent
from plex_v2.factories.paperless import PaperlessPurchasedComponentFactory
from typing import List
from plex_v2.utils.material_pricing_helper import MaterialPricingHelper
from plex_v2.utils.import_utils import ImportUtils
from baseintegration.utils.operations import OperationUtils
import os
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
import yaml
from baseintegration.integration.erp_error_message_converter import ERPErrorMessageConverter


class PLEXPurchasedComponentImporter(PurchasedComponentImporter):

    def _setup_erp_config(self):
        # 1) setup config and client
        self.erp_config, self.plex_client = ERPConfigFactory.create_importer_config(self._integration, 'purchased_components')

        # 2) setup util class
        self._setup_util_classes()

        # setup factories
        self._setup_factories()

        self._setup_error_message_converter()

    def _register_default_processors(self):
        self.register_processor(PurchasedComponent, PurchasedComponentImportProcessor)
        self.register_processor(PurchasedComponentBulkPlaceholder, PurchasedComponentBulkImportProcessor)

    def _register_listener(self):
        self.listener = PLEXPurchasedComponentListener(self._integration, self.erp_config, self.utils)

    def _process_purchased_component(self, pc_id: str):
        with self.process_resource(PurchasedComponent, pc_id) as result:
            return result

    def _bulk_process_purchased_component(self, pc_ids: List[str]):
        with self.process_resource(PurchasedComponentBulkPlaceholder, pc_ids) as result:
            logger.info(f'Bulk processed {len(pc_ids)} purchased components')
            return result

    def _setup_util_classes(self):
        operation_utils: OperationUtils = OperationUtils()
        self.utils: ImportUtils = ImportUtils(self.erp_config, operation_utils)

    def _setup_factories(self):
        material_pricing_helper: MaterialPricingHelper = MaterialPricingHelper(self.utils, self.erp_config)
        self.purchased_component_factory = PaperlessPurchasedComponentFactory(self.erp_config, material_pricing_helper)

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

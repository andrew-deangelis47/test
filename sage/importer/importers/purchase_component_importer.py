from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from sage.importer.importer import SageImporter
from sage.importer.listeners.purchased_component import SagePurchasedComponentsImportListener
from paperless.objects.purchased_components import PurchasedComponent
from sage.importer.processors.purchased_component import SagePurchasedComponentBulkImportProcessor, \
    SagePurchasedComponentImportProcessor, SagePurchasedComponentBulkPlaceholder
from baseintegration.datamigration import logger
from typing import List
from sage.importer.configuration import SagePurchasedComponentConfig


class SagePurchasedComponentImporter(PurchasedComponentImporter, SageImporter):

    def _register_listener(self):
        self.listener = SagePurchasedComponentsImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(PurchasedComponent, SagePurchasedComponentImportProcessor)
        self.register_processor(SagePurchasedComponentBulkPlaceholder, SagePurchasedComponentBulkImportProcessor)
        logger.info('Registered purchased component processor.')

    def _process_purchased_component(self, component_id: str):  # noqa: C901
        logger.info(f"Purchased component id is {str(component_id)}")
        with self.process_resource(PurchasedComponent, component_id):
            logger.info(f"Processed purchased component id: {component_id}")

    def _bulk_process_purchased_component(self, purchased_component_ids: List[str]):
        with self.process_resource(SagePurchasedComponentBulkPlaceholder, purchased_component_ids) as success:
            logger.info(f"Bulk processed {len(purchased_component_ids)} purchased components")
            return success

    def _setup_erp_config(self):
        self.erp_config = SagePurchasedComponentConfig(self._integration.config_yaml)

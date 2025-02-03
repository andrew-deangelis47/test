from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.exporter.order_exporter import logger

from paperless.objects.purchased_components import PurchasedComponent as PaperlessPurchasedComponent

from dynamics.exceptions import DynamicsNotFoundException
from dynamics.importer.utils import DynamicsToPaperlessTranslator, PaperlessObjectCreator
from dynamics.objects.item import PurchasedComponent as DynamicsPurchasedComponent


class DynamicsBulkPurchasedComponentImportProcessor(BaseImportProcessor):
    def _process(self, purchased_component_ids: List[str]) -> bool:
        purchased_component_list = []
        for component_id in purchased_component_ids:
            try:
                dynamics_component: DynamicsPurchasedComponent = DynamicsPurchasedComponent.get_first({"No": component_id})

                purchased_component = PaperlessObjectCreator.empty_purchased_component()
                DynamicsToPaperlessTranslator.update_purchased_component(purchased_component, dynamics_component)

                purchased_component_list.append(purchased_component)
            except DynamicsNotFoundException:
                logger.info(f"Component '{component_id}' not found in Dynamics.")
                continue

        result = PaperlessPurchasedComponent.upsert_many(purchased_component_list)
        return len(result.failures) == 0


class DynamicsPurchasedComponentImportProcessor(DynamicsBulkPurchasedComponentImportProcessor):
    def _process(self, purchased_component_id: str) -> bool:
        return super()._process([purchased_component_id])


class DynamicsPurchasedComponentBulkPlaceholder:
    pass

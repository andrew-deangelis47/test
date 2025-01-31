from ...baseintegration.importer import BaseImporter
from ...baseintegration.exporter.exceptions import IntegrationNotImplementedError
from ...baseintegration.datamigration import logger
from ...baseintegration.integration import Integration
from typing import List


class PurchasedComponentImporter(BaseImporter):
    """Imports purchased components from ERP to Paperless. Should be overriden by an ERP specific importer.
    Requires an ERP specific listener with a "get_new" function"""

    def __init__(self, integration: Integration):
        super().__init__(integration)
        logger.info("Instantiated the purchased component importer")
        self.listener = None
        self._register_listener()
        self.should_create_custom_columns = True

    def run(self, purchased_component_id: str = None):
        logger.info("Calling run for the PurchasedComponentImporter")
        bulk_enable = self.bulk_import_enable("purchased_components")
        method_to_call = getattr(self, '_process_purchased_component')
        if bulk_enable:
            method_to_call = getattr(self, '_bulk_process_purchased_component')
        super().importer_run("purchased_components", method_to_call, "import_purchased_component", False,
                             purchased_component_id, bulk_enable)

    def _process_purchased_component(self, purchased_component_id: str):
        """
        Legacy method to be used sparingly if needed.  The bulk method is preferred.
        :return: The success status of the order processing
        """
        return self._bulk_process_purchased_component([purchased_component_id])

    def _bulk_process_purchased_component(self, purchased_component_ids: List[str]):
        """
        This is the main driver of the whole integration process. This needs to be overridden by the base class
        :return: The success status of the order processing
        """
        raise IntegrationNotImplementedError(
            f"_bulk_process_purchased_component() is not implemented for {self.__class__.__name__}")

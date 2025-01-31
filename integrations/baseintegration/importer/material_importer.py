from ...baseintegration.importer import BaseImporter
from ...baseintegration.exporter.exceptions import IntegrationNotImplementedError
from ...baseintegration.datamigration import logger
from ...baseintegration.integration import Integration
from typing import List


class MaterialImporter(BaseImporter):
    """Imports materials from ERP to Paperless. Should be overriden by an ERP specific importer.
    Requires an ERP specific listener with a "get_new" function"""

    def __init__(self, integration: Integration):
        super().__init__(integration)
        logger.info("Instantiated the material importer")
        self.listener = None
        self._register_listener()

    def run(self, material_id: str = None):
        logger.info("Calling run for the MaterialImporter")
        bulk_enable = self.bulk_import_enable("materials")
        method_to_call = getattr(self, '_process_material')
        if bulk_enable:
            method_to_call = getattr(self, '_bulk_process_material')
        super().importer_run("materials", method_to_call, "import_material", True, material_id, bulk_enable)

    def check_custom_table_exists(self):
        raise IntegrationNotImplementedError(f"check_custom_table_exists() is not implemented for {self.__class__.__name__}")

    def _process_material(self, material_id: str):
        """
        Legacy method to be used sparingly if needed.  The bulk method is preferred.
        :return: The success status of the order processing
        """
        return self._bulk_process_material([material_id])

    def _bulk_process_material(self, material_ids: List[str]):
        """
        This is the main driver of the whole integration process. This needs to be overridden by the base class
        :return: The success status of the order processing
        """
        raise IntegrationNotImplementedError(f"_bulk_process_material() is not implemented for {self.__class__.__name__}")

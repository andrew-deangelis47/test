from ...baseintegration.importer import BaseImporter
from ...baseintegration.exporter.exceptions import IntegrationNotImplementedError
from ...baseintegration.datamigration import logger
from ...baseintegration.integration import Integration


class MaterialPricingImporter(BaseImporter):

    def __init__(self, integration: Integration):
        super().__init__(integration)
        logger.info("Instantiated the material pricing importer")
        self.listener = None
        self._register_listener()

    def run(self, quote_id: str = None):
        logger.info("Calling run for the MaterialPricingImporter")
        method_to_call = getattr(self, '_process_material_pricing')
        super().importer_run("material_pricing", method_to_call, "import_material_pricing", True, quote_id, False)

    def _process_material_pricing(self, quote_id: str):
        """
        This is the main driver of the whole integration process. This needs to be overridden by the base class
        :return: The success status of the quote processing
        """
        raise IntegrationNotImplementedError(f"_process_material_pricing() is not implemented for {self.__class__.__name__}")

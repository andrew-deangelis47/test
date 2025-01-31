from ...baseintegration.importer import BaseImporter
from ...baseintegration.exporter.exceptions import IntegrationNotImplementedError
from ...baseintegration.datamigration import logger
from ...baseintegration.integration import Integration
from typing import List


class OutsideServiceImporter(BaseImporter):
    """Imports work_centers from ERP to Paperless. Should be overriden by an ERP specific importer.
    Requires an ERP specific listener with a "get_new" function"""

    def __init__(self, integration: Integration):
        super().__init__(integration)
        logger.info("Instantiated the outside_service importer")
        self.listener = None
        self._register_listener()

    def run(self, service_id: str = None):
        logger.info("Calling run for the ServiceImporter")
        method_to_call = getattr(self, '_process_outside_service')
        bulk_enable = self.bulk_import_enable("outside_services")
        if bulk_enable:
            method_to_call = getattr(self, '_bulk_process_outside_services')
        super().importer_run("outside_services", method_to_call, "import_service", True, service_id)

    def check_custom_table_exists(self):
        raise IntegrationNotImplementedError(
            f"check_custom_table_exists() is not implemented for {self.__class__.__name__}")

    def _process_outside_service(self, service_id: str):
        """
        Legacy method to be used sparingly if needed.  The bulk method is preferred.
        :return: The success status of the order processing
        """
        return self._bulk_process_outside_services(service_ids=[service_id])

    def _bulk_process_outside_services(self, service_ids: List[str]):
        """
        This is the main driver of the whole integration process. This needs to be overridden by the base class
        :return: The success status of the order processing
        """
        raise IntegrationNotImplementedError(f"_bulk_process_outside_services() is not implemented for {self.__class__.__name__}")

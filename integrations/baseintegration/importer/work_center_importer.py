from ...baseintegration.importer import BaseImporter
from ...baseintegration.exporter.exceptions import IntegrationNotImplementedError
from ...baseintegration.datamigration import logger
from ...baseintegration.integration import Integration
from typing import List


class WorkCenterImporter(BaseImporter):
    """Imports work_centers from ERP to Paperless. Should be overriden by an ERP specific importer.
    Requires an ERP specific listener with a "get_new" function"""

    def __init__(self, integration: Integration):
        super().__init__(integration)
        logger.info("Instantiated the work_center importer")
        self.listener = None
        self._register_listener()

    def run(self, work_center_id: str = None):
        logger.info("Calling run for the WorkCenterImporter")
        bulk_enable = self.bulk_import_enable("work_centers")
        method_to_call = getattr(self, '_process_work_center')
        if bulk_enable:
            method_to_call = getattr(self, '_bulk_process_work_center')
        super().importer_run("work_centers", method_to_call, "import_work_center", True, work_center_id, bulk_enable)

    def check_custom_table_exists(self):
        raise IntegrationNotImplementedError(f"register_listener() is not implemented for {self.__class__.__name__}")

    def _process_work_center(self, work_center_id: str):
        """
        Legacy method to be used sparingly if needed.  The bulk method is preferred.
        :return: The success status of the order processing
        """
        return self._bulk_process_work_center([work_center_id])

    def _bulk_process_work_center(self, work_center_ids: List[str]):
        """
        This is the main driver of the whole integration process. This needs to be overridden by the base class
        :return: The success status of the order processing
        """
        raise IntegrationNotImplementedError(f"_bulk_process_work_center() is not implemented for {self.__class__.__name__}")

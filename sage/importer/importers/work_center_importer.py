from baseintegration.importer.work_center_importer import WorkCenterImporter
from sage.importer.importer import SageImporter
from sage.models.paperless_custom_tables.work_centers import WorkCenter
from sage.models.paperless_custom_tables.standard_operation import StandardOperation
from baseintegration.datamigration import logger
from typing import List
from sage.importer.configuration import SageWorkCenterConfig
from sage.importer.listeners.work_centers import SageWorkCenterImportListener
from baseintegration.utils import Workcenter
from sage.importer.processors.work_centers import SageBulkWorkCenterImportProcessor, \
    SageWorkCenterBulkPlaceholder, SageWorkCenterImportProcessor


class SageWorkCenterImporter(WorkCenterImporter, SageImporter):
    _paperless_table_model_work_centers = WorkCenter()
    _paperless_table_model_standard_operations = StandardOperation()

    def _register_listener(self):
        self.listener = SageWorkCenterImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Workcenter, SageWorkCenterImportProcessor)
        self.register_processor(SageWorkCenterBulkPlaceholder, SageBulkWorkCenterImportProcessor)
        logger.info('Registered work center processor.')

    def _process_work_center(self, work_center_id: str):  # noqa: C901
        logger.info(f"Work center id is {str(work_center_id)}")
        with self.process_resource(Workcenter, work_center_id):
            logger.info(f"Processed work center id: {work_center_id}")

    def _bulk_process_work_center(self, work_center_ids: List[str]):  # noqa: C901
        with self.process_resource(SageWorkCenterBulkPlaceholder, work_center_ids) as success:
            logger.info(f"Bulk processed {len(work_center_ids)} work centers")
            return success

    def _setup_erp_config(self):
        self.erp_config = SageWorkCenterConfig(self._integration.config_yaml)

    def check_custom_table_exists(self):
        self.add_or_remove_custom_table_attributes()
        self._paperless_table_model_work_centers.check_custom_header_custom_table_exists()
        self._paperless_table_model_standard_operations.check_custom_header_custom_table_exists()

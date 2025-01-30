from baseintegration.datamigration import logger
from baseintegration.importer.work_center_importer import WorkCenterImporter
from plex_v2.configuration import ERPConfigFactory
from plex_v2.importer.listeners import PLEXWorkCenterListener
from plex_v2.importer.processors import WorkCenterImportProcessor, WorkCenterBulkImportProcessor, WorkCenterBulkPlaceholder
from typing import List
from plex_v2.objects.work_center_custom_table import WorkCenterCustomTable
from plex_v2.factories.paperless import WorkCenterCustomTableRowFactory
from integrations.baseintegration.utils import Workcenter
import os
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
import yaml
from baseintegration.integration.erp_error_message_converter import ERPErrorMessageConverter


class PLEXWorkCenterImporter(WorkCenterImporter):

    def _setup_erp_config(self):
        self.erp_config, self.plex_client = ERPConfigFactory.create_importer_config(self._integration, 'work_centers')
        self._paperless_table_model = WorkCenterCustomTable()

        # setup factories
        self.work_center_custom_table_row_factory = WorkCenterCustomTableRowFactory(self.erp_config)

        self._setup_error_message_converter()

    def _register_default_processors(self):
        self.register_processor(Workcenter, WorkCenterImportProcessor)
        self.register_processor(WorkCenterBulkPlaceholder, WorkCenterBulkImportProcessor)

    def _register_listener(self):
        self.listener = PLEXWorkCenterListener(self._integration, self.erp_config)

    def _process_work_center(self, work_center_code: str):
        with self.process_resource(Workcenter, work_center_code) as result:
            return result

    def _bulk_process_work_center(self, work_center_codes: List[str]):  # noqa: C901
        with self.process_resource(WorkCenterBulkPlaceholder, work_center_codes) as success:
            logger.info(f"Bulk processed {len(work_center_codes)} work centers")
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

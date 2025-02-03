from baseintegration.importer import BaseImporter
from baseintegration.exporter.exceptions import IntegrationNotImplementedError
from baseintegration.datamigration import logger
from baseintegration.integration import Integration
from baseintegration.utils.custom_table import ImportCustomTable
from typing import List


class CustomTableRecordImporter(BaseImporter):
    """Imports materials from ERP to Paperless. Should be overriden by an ERP specific importer.
    Requires an ERP specific listener with a "get_new" function"""

    def __init__(self, integration: Integration):
        super().__init__(integration)
        logger.info("Instantiated the custom table record importer")
        self.listener = None
        self.header_dict = self._integration.config_yaml["Importers"]["custom_table"].get("header_dict")
        self.custom_table_name = self._integration.config_yaml["Importers"]["custom_table"].get("custom_table_name")
        self.id_field = self._integration.config_yaml["Importers"]["custom_table"].get("id_field", None)
        self._register_listener()

    def run(self, record_id: str = None):
        logger.info("Calling run for the CustomTableRecordImporter")
        method_to_call = getattr(self, '_process_record')
        bulk_enable = self.bulk_import_enable("custom_table")
        if bulk_enable:
            method_to_call = getattr(self, '_bulk_process_records')
        super().importer_run("custom_table_record", method_to_call, "import_custom_table_record", True, record_id)

    def _register_listener(self):
        raise IntegrationNotImplementedError(f"register_listener() is not implemented for {self.__class__.__name__}")

    def check_custom_table_exists(self):
        return ImportCustomTable.check_custom_header_custom_table_exists(self.custom_table_name, self.header_dict,
                                                                         self.id_field)

    def _process_record(self, record_id: str) -> bool:
        """
        Legacy method to be used sparingly if needed.  The bulk method is preferred.
        :return: The success status
        """
        return self._bulk_process_records(record_ids=[record_id])

    def _bulk_process_records(self, record_ids: List[str]):
        """
        This is the main driver of the whole integration process. This needs to be overridden by the base class
        :return: The success status
        """
        raise IntegrationNotImplementedError(f"_process_record() is not implemented for {self.__class__.__name__}")


class CustomTableBulkPlaceholder:
    pass

from typing import Optional

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import custom_table_patch
from baseintegration.utils.custom_table import ImportCustomTable
from paperless.client import PaperlessClient


class CustomTableRecordImportProcessor(BaseImportProcessor):

    def _process(self, record_id: str):
        logger.info("Calling process method")
        custom_table_dict = self.get_custom_table_dict(record_id, self._importer.header_dict)
        if custom_table_dict:
            logger.info("Customer table dict:")
            logger.info(custom_table_dict)
            headers = ImportCustomTable.assemble_custom_headers(custom_table_dict)
            new_record = ImportCustomTable.generate_custom_header_nr(custom_table_dict, headers)
            data = dict(row_data=new_record)
            client = PaperlessClient.get_instance()
            url = f'suppliers/public/custom_tables/{self.get_custom_table_name()}/row'
            custom_table_patch(client=client, data=data, url=url, identifier=record_id)

    def get_custom_table_dict(self, record_id: str, header_dict) -> Optional[dict]:
        return None

    def get_custom_table_name(self) -> str:
        return self._importer._integration.config_yaml["Importers"]["custom_table"].get("custom_table_name", 'custom_table')

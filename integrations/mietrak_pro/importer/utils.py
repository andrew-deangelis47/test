from typing import List
from baseintegration.datamigration import logger
from baseintegration.exporter import IntegrationNotImplementedError
from baseintegration.importer.import_processor import BaseImportProcessor

from baseintegration.utils.custom_table import ImportCustomTable, HexImportCustomTable
from baseintegration.utils import custom_table_put
from paperless.client import PaperlessClient


class MieTrakProCustomTableBulkImportProcessor(BaseImportProcessor):

    def _process(self, entity_ids: List[int]):
        self.update_custom_table(entity_ids=entity_ids)

    def _get_row_data(self, entity_id: int) -> dict:
        raise IntegrationNotImplementedError(f"_get_row_data() is not implemented for {self.__class__.__name__}")

    def update_custom_table(self, entity_ids):
        new_records = []
        for entity_id in entity_ids:
            new_record = self.create_new_record(entity_id=entity_id)
            new_records.append(new_record.copy())
        data = dict(rows=new_records)
        client = PaperlessClient.get_instance()
        url = f"suppliers/public/custom_tables/{self._importer.table_name}/row/bulk"
        result = custom_table_put(client=client, data=data, url=url, identifier=str(entity_id))
        logger.info(f'Result of put -> {result}')

    def create_new_record(self, entity_id):
        dict_to_upload = self._importer.header_dict.copy()
        row_data = self._get_row_data(entity_id)
        row_data = {k: v for k, v in row_data.items() if v is not None}  # filter out None values
        dict_to_upload.update(row_data)
        if dict_to_upload:
            headers = ImportCustomTable.assemble_custom_headers(dict_to_upload)
            new_record = ImportCustomTable.generate_custom_header_nr(dict_to_upload, headers)
            return new_record
        return None


class MieTrakProCustomTableImportProcessor(MieTrakProCustomTableBulkImportProcessor):

    def _process(self, entity_id: int):
        self.update_custom_table(entity_ids=[entity_id])


class MietrakProImportListener:
    def __init__(self, integration, identifier, config_key, importer_plural):
        self.identifier = identifier
        self._integration = integration
        self.config_key = config_key
        self.importer_plural = importer_plural
        logger.info(f"MIE Trak Pro {importer_plural} import listener was instantiated")

    def get_new(self, bulk=False) -> set:
        ids = set()
        logger.info(f"Checking for new {self.importer_plural}")
        last_processed_hex_counter = HexImportCustomTable.get_last_processed_hex_counter(self.identifier)
        new_hex_counter = last_processed_hex_counter
        last_processed_decimal_counter = int(last_processed_hex_counter, 16)

        minimum_primary_key_value = \
            self._integration.config_yaml["Importers"][self.config_key].get("minimum_primary_key_value", 0)

        new_hex_counter = self._add_new_ids(ids, new_hex_counter, last_processed_decimal_counter,
                                            minimum_primary_key_value)

        logger.info(f"Found {len(ids)} records to update")
        HexImportCustomTable.update_last_processed_hex_counter(self.identifier, new_hex_counter)
        return ids

    def _add_new_ids(self, ids, new_hex_counter: str, last_processed_decimal_counter: int,
                     minimum_primary_key_value) -> str:
        """
        Adds IDs of new entities to ids param. Returns the updated hex counter.
        """
        query = self._get_new_query(last_processed_decimal_counter, minimum_primary_key_value)
        return self._add_ids_from_query(ids, new_hex_counter, query)

    def _get_new_query(self, last_processed_decimal_counter: int, minimum_primary_key_value) -> str:
        """
        Returns the SQL query for new entities. Should be overridden if a single query is required to retrieve new
        entities. If multiple queries are required, override _add_new_ids instead.
        """
        raise IntegrationNotImplementedError(f"_get_new_query() is not implemented for {self.__class__.__name__}")

    @classmethod
    def _add_ids_from_query(cls, id_list: set, new_hex_counter: str, query: str) -> str:
        """
        Executes a given query, adding results to the given list and returning the new hex counter.
        """
        # Use a raw SQL query to get the records newer than the last processed counter.
        # LastAccess field is not included on the Django model because it caused issues when creating new objects
        # (the LastAccess field is a rowversion / timestamp field and as such its value cannot be set manually,
        # it must be updated by SQL Server)
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            # Pyodbc returns bytes objects for the LastAccess field, we want to convert these to a hexadecimal
            # string representation
            hex_counter_pairs = [(pk, f'0x{b.hex()}') for (pk, b) in results]
        for entity_id, hex_counter in hex_counter_pairs:
            id_list.add(entity_id)
            if int(hex_counter, 16) > int(new_hex_counter, 16):
                new_hex_counter = hex_counter

        return new_hex_counter

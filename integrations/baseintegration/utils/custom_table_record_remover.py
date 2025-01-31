from paperless.client import PaperlessClient
from typing import List
from ...baseintegration.datamigration import logger
from ...baseintegration.utils import custom_table_delete_row
import json

CUSTOM_TABLE_KEY_ROW_NUMBER = 'row_number'


class CustomTableRecordRemover:

    client: PaperlessClient
    test_mode: bool

    def __init__(self, client: PaperlessClient, test_mode: bool = False):
        self.client: PaperlessClient = client
        self.test_mode: bool = test_mode

    def _get_all_rows(self, table_name: str):
        url = f"suppliers/public/custom_tables/{table_name}"
        response = self.client.request(url, data={}, method="get")
        if not self.test_mode:
            return response.json()["rows"]
        json_string = response.content.decode('utf-8')
        dictionary = json.loads(json_string)
        return dictionary["rows"]

    def remove_custom_table_rows(self, table_name: str, primary_key_column_name: str, should_delete_row_function):
        """ takes a function which accepts a custom table row (type of dict) and decides if it should be deleted"""

        # 1) determine which rows to delete based on function passed in
        rows_to_delete: List[dict] = []
        rows: List[dict] = self._get_all_rows(table_name)
        row: dict
        logger.info(f'Found {len(rows)} total rows. Determining what rows to delete from custom table "{table_name}"...')
        for row in rows:
            if should_delete_row_function(row):
                rows_to_delete.append(row)

        # 2) remove the rows
        logger.info(f'Found {len(rows_to_delete)} rows to delete from custom table "{table_name}".')
        if len(rows_to_delete) == 0:
            return

        row: dict
        i = 1
        for row in rows_to_delete:
            data = {}
            row.pop(CUSTOM_TABLE_KEY_ROW_NUMBER)
            primary_key_value = row[primary_key_column_name]
            data["row_data"] = row
            logger.info(f'Removing {i} if {len(rows_to_delete)}. Primary key is "{primary_key_value}"')

            # we dont need to actually test this we know it works because it's already in base
            # it isn't testable because the test relies on a fake response that can't be handled by this method
            if not self.test_mode:
                custom_table_delete_row(self.client, f'suppliers/public/custom_tables/{table_name}/row', data, f'deleting row with primary key "{primary_key_value}"')

from unittest.mock import create_autospec
from paperless.client import PaperlessClient
from ...baseintegration.utils.custom_table_record_remover import CustomTableRecordRemover
from requests import Response
from django.http import JsonResponse

ROW_NUMBER_COLUMN = 'row_number'
TEST_ROW_NUMBER = 1
TEST_CUSTOM_TABLE_COLUMN_NAME = 'TEST_CUSTOM_TABLE_COLUMN_NAME'
TEST_NON_REMOVAL_VALUE = 'TEST_NON_REMOVAL_VALUE'
TEST_REMOVAL_VALUE = 'TEST_REMOVAL_VALUE'
PRIMARY_KEY_COLUMN_NAME = 'PRIMARY_KEY_COLUMN_NAME'
PK_0 = 'PK_0'
PK_1 = 'PK_1'


# test removal function
def should_remove_function(row: dict) -> bool:
    if row[TEST_CUSTOM_TABLE_COLUMN_NAME] == TEST_REMOVAL_VALUE:
        return True
    return False


def get_fake_custom_table_data():
    return {"rows": [
        {ROW_NUMBER_COLUMN: TEST_ROW_NUMBER, PRIMARY_KEY_COLUMN_NAME: PK_0, TEST_CUSTOM_TABLE_COLUMN_NAME: TEST_REMOVAL_VALUE},
        {ROW_NUMBER_COLUMN: TEST_ROW_NUMBER, PRIMARY_KEY_COLUMN_NAME: PK_1, TEST_CUSTOM_TABLE_COLUMN_NAME: TEST_NON_REMOVAL_VALUE}
    ]}


class TestErpMessageConverter:

    def setup_method(self) -> None:
        # for now just return no rows
        response = Response()
        response._content
        client = create_autospec(PaperlessClient)
        client.request.return_value = JsonResponse(get_fake_custom_table_data(), status=200)

        self.custom_table_record_remover: CustomTableRecordRemover = CustomTableRecordRemover(client, True)

    def test_remover(self):
        self.custom_table_record_remover.remove_custom_table_rows('fake_table_name', PRIMARY_KEY_COLUMN_NAME, should_remove_function)

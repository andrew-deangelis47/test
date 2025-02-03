from baseintegration.datamigration import logger
from paperless.client import PaperlessClient
from baseintegration.utils import custom_table_patch
from baseintegration.integration import Integration
from pydantic import Field

from typing import Dict, Any, Union, List
from baseintegration.utils.custom_table import ImportCustomTable
from paperless.objects.orders import Order
from paperless.objects.quotes import Quote
from pendulum.datetime import DateTime
from pytz import timezone
from baseintegration.utils import custom_table_delete_row

COLUMN_NAME_EXPORT_ID = 'export_id'
COLUMN_NAME_QUOTE_NUM = 'quote_num'
COLUMN_NAME_QUOTE_REV = 'quote_rev'
COLUMN_NAME_ORDER_NUM = 'order_num'

CUSTOM_TABLE_KEY_ROW_NUMBER = 'row_number'


class IntegrationExportReportCustomTable:
    _custom_table_name: str = 'integration_export_report'
    _primary_key: str = 'export_id'

    @staticmethod
    def replaced_type(value_type):
        if value_type == str:
            return "str"
        elif value_type == float:
            return 1.0
        elif value_type == int:
            return 0
        elif value_type == bool:
            return True

    def create_paperless_table_header_sample(self, ) -> Dict[str, Any]:  # Dict["column_name", "value_type"]
        """
        Assembles header sample without _custom_table_name as a column header.
        """
        result: dict = {}
        for key, field in self.__dict__.items():
            if key == "_custom_table_name":
                continue
            result[key] = self.replaced_type(type(field))
        return result

    def check_custom_header_custom_table_exists(self):
        primary_key = self._primary_key
        table_name = self._custom_table_name
        header_sample: Dict[str, Any] = self.create_paperless_table_header_sample()
        ImportCustomTable.check_custom_header_custom_table_exists(name=table_name,
                                                                  header_dict=header_sample,
                                                                  id_fields=[primary_key])


class IntegrationExportReport:
    export_id: str
    order_num: str
    quote_num: str
    quote_revision: str
    custom_table_columns: dict  # representation of the data in the custom table row
    custom_table: IntegrationExportReportCustomTable

    def __init__(self, integration: Integration, exporter_type: Union[Order, Quote], test_mode: bool = False):
        # 1) read in the configured column names
        configured_columns = integration.config_yaml.get("integration_report_columns", None)
        row_count_limit = integration.config_yaml.get("integration_report_row_limit", None)
        clear_count = integration.config_yaml.get("integration_report_clear_count", None)

        if configured_columns is None:
            logger.info('Config option "integration_report_columns" is not set up, will not create integration report')
            return
        if row_count_limit is None:
            logger.info('Config option "integration_report_row_limit" is not set up, will not create integration report')
            return
        if clear_count is None:
            logger.info('Config option "clear_count" is not set up, will not create integration report')
            return

        # 2) setup class properties to represent custom table columns
        self._setup_mandatory_properties(exporter_type)
        self._setup_configurable_properties(exporter_type, configured_columns)

        # 3) create table if not already exists (if it's in test mode we wont actually create the table)
        if not test_mode:
            self.custom_table.check_custom_header_custom_table_exists()
            self._clear_oldest_rows_if_needed(row_count_limit, clear_count)
            logger.info(f'Instantiated integration report row for export with ID: "{self.export_id}"')
            self.update_table()

    def _setup_mandatory_properties(self, exporter_type: Union[Order, Quote]) -> None:
        """
        Set's certain properties which each represent a column in the report
        Mandatory columns: export id, either order number or quote number and revision
        Configurable: whatever is defined in "integration_report_columns" in the config
        """
        is_order_export = isinstance(exporter_type, Order)

        # mandatory properties
        if is_order_export:
            order: Order = exporter_type
            self.export_id = self._get_export_id_from_order(order)
            self.order_num = str(order.number)
        else:
            quote: Quote = exporter_type
            self.export_id = self._get_export_id_from_quote(quote)
            self.quote_num = str(quote.number)
            revision = '' if quote.revision_number is None else quote.revision_number
            self.quote_revision = str(revision)

    def _setup_configurable_properties(self, exporter_type: Union[Order, Quote], configured_columns: List[str]):
        custom_table_columns = {}
        custom_table = IntegrationExportReportCustomTable()
        is_order_export = isinstance(exporter_type, Order)

        # set the export id in the table
        custom_table_columns[COLUMN_NAME_EXPORT_ID] = self.export_id
        setattr(custom_table, COLUMN_NAME_EXPORT_ID, self.export_id)

        # order vs quote identifiers
        if is_order_export:
            custom_table_columns[COLUMN_NAME_ORDER_NUM] = self.order_num
            setattr(custom_table, COLUMN_NAME_ORDER_NUM, self.order_num)
        else:
            custom_table_columns[COLUMN_NAME_QUOTE_NUM] = self.quote_num
            custom_table_columns[COLUMN_NAME_QUOTE_REV] = self.quote_revision
            setattr(custom_table, COLUMN_NAME_QUOTE_NUM, exporter_type.number)
            revision_number = '' if exporter_type.revision_number is None else exporter_type.revision_number
            setattr(custom_table, COLUMN_NAME_QUOTE_REV, revision_number)

        # configured columns
        for column_name in configured_columns:
            logger.info('alias = ' + str(column_name))
            field: str = Field(alias=str(column_name))
            setattr(custom_table, str(column_name), field)
            custom_table_columns[str(column_name)] = ''

        self.custom_table_columns = custom_table_columns
        self.custom_table = custom_table

    def _get_export_id_from_order(self, order: Order) -> str:
        export_id = f'Order #{str(order.number)} '
        export_id += self._get_current_time()
        return export_id

    def _get_export_id_from_quote(self, quote: Quote) -> str:
        export_id = f'Quote #{str(quote.number)}'
        rev = quote.revision_number
        full_revision: str
        if rev is None:
            full_revision = " "
        else:
            full_revision = f'-{rev} '

        export_id += full_revision
        export_id += self._get_current_time()
        return export_id

    def update_table(self):
        try:
            url = f"suppliers/public/custom_tables/{self.custom_table._custom_table_name}/row"
            paperless_client = PaperlessClient.get_instance()
            custom_table_patch(client=paperless_client, data=dict(row_data=self._to_dict()), url=url,
                               identifier='updating integration report')
        # catch the case where the report isnt set up in config but it still tries to update - just continue
        except (AttributeError, KeyError, Exception):
            logger.info('The integration report custom table is misconfigured. Please make sure the columns in the config match the columns in the existing table. Also check that the columns each processor'
                        ' writes to exists in the config.')
            pass

    def _clear_oldest_rows_if_needed(self, row_count_limit: int, clear_count: int) -> None:
        # 1) get all the rows
        url = f"suppliers/public/custom_tables/{self.custom_table._custom_table_name}"
        client = PaperlessClient.get_instance()
        response = client.request(url, data={}, method="get")
        rows = response.json()["rows"]
        if len(rows) >= row_count_limit:

            # 1) get the rows in order from oldest to most recent
            rows_to_delete = sorted(rows, key=lambda x: x[CUSTOM_TABLE_KEY_ROW_NUMBER])

            # 2) grab the clear_count amount of oldest rows to delete
            rows_to_delete = rows_to_delete[:clear_count]

            # 3) loop through and delete each row
            url += '/row'
            for row in rows_to_delete:
                # construct the payload
                dict = {}
                row_number = row[CUSTOM_TABLE_KEY_ROW_NUMBER]
                row.pop(CUSTOM_TABLE_KEY_ROW_NUMBER)
                dict['row_data'] = row

                custom_table_delete_row(client=client, data=dict, url=url,
                                        identifier=f'clearing out row number {row_number} because table hit limit of {row_count_limit}')
            # log out the total rows removed for clarity
            if len(rows_to_delete) > 0:
                logger.info(f'Cleared {len(rows_to_delete)} rows total')

    def _to_dict(self):
        return self.custom_table_columns

    def add_message(self, key: str, value: str):
        try:
            value = value + "\r\n"
            existing_val = self.custom_table_columns[key]
            value = existing_val + value
            self.custom_table_columns[key] = value

        # handle if we try to use this but it is not setup in config, just ignore
        except (AttributeError, KeyError):
            return

    def _get_current_time(self) -> str:
        tz = timezone('EST5EDT')
        return (str(DateTime.now(tz))[0:19]).replace('T', ' ')

from typing import Tuple, List, Union, Dict, Any

from django.db.models.expressions import RawSQL

from ...baseintegration.datamigration import logger
from paperless.custom_tables.custom_tables import CustomTable
from paperless.exceptions import PaperlessException, PaperlessNotFoundException
from paperless.client import PaperlessClient
from datetime import date, datetime, timedelta
from decimal import Decimal
from django.db.models import Model
from django.utils.datastructures import ImmutableList
from django.db.models.fields import BooleanField, DecimalField, IntegerField
import pendulum
import time

from ...baseintegration.utils import custom_table_put, custom_table_delete_row, get_dict_size

NUMERIC = 'numeric'
BOOL = 'boolean'
STRING = 'string'
TYPES = [NUMERIC, BOOL, STRING]

MAX_BATCH_SIZE = 1000
MAX_UPLOAD_SIZE_MB = 2.5


class ImportCustomTable:
    """This class contains utility methods for working with Paperless parts custom tables"""

    @staticmethod
    def import_from_django_model(model: Model, name: str, recreate: bool = False, generate_table_data: bool = True,
                                 id_fields: Union[str, List[str]] = []):
        """
        A function which, given a Django model, will upload a custom table (either empty or with the data)

        @param model: a Django model
        @param name: a string representing what you want your custom table to be called
        @param recreate: a boolean representing whether or not you want to delete an existing table and re-upload it
        @param generate_table_data: a boolean representing whether or not you want the contents of the database as rows in the table
        @param id_fields: a list strings or single string representing the field name of the primary key in the table
        @return: boolean
        """

        if not isinstance(id_fields, list):
            id_fields = [id_fields]

        config, headers = ImportCustomTable.convert_datastructures(model, id_fields)
        if generate_table_data:
            data = ImportCustomTable.generate_table_data(model, headers)
        else:
            data = []
        return ImportCustomTable.upload_custom_table(config, data, name, recreate)

    @staticmethod
    def import_from_custom_dict(custom_dict: dict, name: str, recreate: bool = False, generate_table_data: bool = True,
                                id_fields: Union[str, List[str]] = []):
        """
        A function which, given a dictionary of example values, will upload a custom table (either empty or with the data)

        @param custom_dict: a dictionary with key/value pairs {"col": "value"} - for example {"material_id": "123", "qty_on_hand": 10}
        @param name: a string representing what you want your custom table to be called
        @param recreate: a boolean representing whether or not you want to delete an existing table and re-upload it
        @param generate_table_data: a boolean representing whether or not you want the contents of the database as rows in the table
        @param id_field: a string representing the field name of the primary key in the table
        @return: boolean
        """

        if not isinstance(id_fields, list):
            id_fields = [id_fields]

        config, headers = ImportCustomTable.convert_dict(custom_dict, id_fields)
        if generate_table_data:
            data = ImportCustomTable.generate_custom_header_table_data(custom_dict, headers)
        else:
            data = []
        return ImportCustomTable.upload_custom_table(config, data, name, recreate)

    @staticmethod
    def convert_datastructures(model: Model, id_fields: List[str] = []) -> Tuple:
        """
        A function which gets a custom table configuration and headers from a Django model

        @param model: a Django model
        @param id_fields: a list of strings representing the field name of the primary key in the table
        @return: tuple
        """
        fields = model._meta.fields
        headers = ImportCustomTable.assemble_headers(fields)
        config = ImportCustomTable.assemble_config(headers, id_fields)
        return config, headers

    @staticmethod
    def convert_dict(custom_dict: dict, id_fields: List[str] = []) -> Tuple:
        """
        A function which gets a custom table configuration and headers from a custom dictionary

        @param custom_dict: a dictionary with key/value pairs {"col": "value"} - for example {"material_id": "123", "qty_on_hand": 10}
        @param id_fields: a list of strings representing the field name of the primary key in the table
        @return: tuple
        """
        headers = ImportCustomTable.assemble_custom_headers(custom_dict)
        config = ImportCustomTable.assemble_config(headers, id_fields)
        return config, headers

    @staticmethod
    def assemble_headers(fields: ImmutableList) -> list:
        headers = []
        for field in fields:
            var_str = f"{field}"
            split = var_str.split('.')
            value_name = split[-1]
            value_type = ImportCustomTable.get_column_type(type(field))
            headers.append([value_name, value_type])
        logger.info('Created headers.')
        return headers

    @staticmethod
    def assemble_custom_headers(custom_dict: dict):
        headers = []
        for header, value in custom_dict.items():
            if isinstance(value, (int, float)):
                value_type = NUMERIC
            elif isinstance(value, bool):
                value_type = BOOL
            else:
                value_type = STRING
            headers.append([header, value_type])
        return headers

    @staticmethod
    def get_column_type(column_type) -> str:
        if column_type in [DecimalField, IntegerField]:
            return NUMERIC
        elif column_type == BooleanField:
            return BOOL
        else:
            return STRING

    @staticmethod
    def assemble_config(headers, id_fields: List[str] = []) -> list:
        """
        A function which creates the config necessary for creating a custom table in Paperless parts

        @param headers: a list containing table columns with their types
        @param id_fields: a list of strings representing the field name of the primary key in the table
        @return: A list of dictionaries containing column names, value types, and whether or not it is a primary key
        """
        config = []
        for pair in headers:
            if id_fields and pair[0] in id_fields:
                is_for_unique_key = True
            else:
                is_for_unique_key = False
            config.append(dict(column_name=pair[0], value_type=pair[1], is_for_unique_key=is_for_unique_key))
        logger.info(f'Created config options:{config}')
        return config

    @staticmethod
    def generate_table_data(model: Model, headers: list):
        table = []
        rows = model.objects.all()
        for row in rows:
            nr = ImportCustomTable.generate_nr(row, headers)
            table.append(nr)
        return table

    @staticmethod
    def generate_custom_header_table_data(custom_dict: dict, headers: list):
        nr = ImportCustomTable.generate_custom_header_nr(custom_dict, headers)
        return nr

    @staticmethod
    def generate_nr(row, headers):
        nr = dict()
        for pair in headers:
            value = getattr(row, pair[0])
            if isinstance(value, Decimal):
                nr[pair[0]] = round(float(value), 3) if value is not None else 0
            elif isinstance(value, (date, datetime)):
                nr[pair[0]] = datetime.strftime(value, '%Y-%m-%d %H:%M:%S') if value is not None else 0
            else:
                nr[pair[0]] = value if value is not None else 0
        return nr

    @staticmethod
    def generate_custom_header_nr(custom_dict, headers):
        nr = dict()
        for pair in headers:
            value = custom_dict[pair[0]]
            if isinstance(value, Decimal):
                nr[pair[0]] = round(float(value), 3) if value is not None else 0
            elif isinstance(value, (date, datetime)):
                nr[pair[0]] = datetime.strftime(value, '%Y-%m-%d %H:%M:%S') if value is not None else 0
            else:
                nr[pair[0]] = value if value is not None else 0
        return nr

    @staticmethod
    def upload_custom_table(config, table_data, table_name, recreate: bool = False):
        """
        A function which uploads a custom table to a Paperless account

        @param config: a list of dictionaries which defines each column and each column's type
        @param table_data: a list of dictionaries which defines the values for each row
        @param table_name: the name of the custom table
        @param recreate: whether or not the custom table should be deleted if it already exists
        @return: boolean - whether it succeeded
        """
        table = CustomTable(data=table_data)
        logger.info(f"Uploading custom table {table_name}, recreate {recreate} with data: {table_data}")
        CustomTable.config = config
        try:
            table_list = CustomTable.get_list()
            if table_name not in table_list:
                table.create(table_name)
            if table_name in table_list and recreate:
                table.delete(table_name)
                table.create(table_name)
            try:
                table.update(table_name)
            except PaperlessException as e:
                if "duplicate key value violates unique constraint" in str(e):
                    logger.info(f"Was not able to upload {table_name} first time, trying again after 10s")
                    time.sleep(10)
                    table.update(table_name)
                else:
                    raise e
            logger.info(f'Table uploaded as "{table_name}" successfully!\n\n')
            return True
        except Exception as e:
            logger.info(e)
            logger.error(f'Error: Table upload failed for "{table_name}". Account Custom Table configuration needs to '
                         f'be checked')
            return False

    @staticmethod
    def upload_records(identifier: str, records: List[dict], table_name: str) -> dict:
        total_results = {"failures": [],
                         "successes": []}
        record_batch = []

        def post_rows(rows: list):
            if not rows:
                return
            batch = dict(rows=rows)
            client = PaperlessClient.get_instance()
            url = f"suppliers/public/custom_tables/{table_name}/row/bulk"
            result = custom_table_put(client=client, data=batch, url=url, identifier=identifier)
            fails = result.get("failures", [])
            success = result.get("successes", [])
            total_results["failures"] = total_results["failures"] + fails
            total_results["successes"] = total_results["successes"] + success

        for record in records:
            data_with_new_record = dict(rows=[*record_batch, record])
            if len(record_batch) >= MAX_BATCH_SIZE or get_dict_size(data_with_new_record) >= MAX_UPLOAD_SIZE_MB:
                post_rows(record_batch)
                record_batch = []
            record_batch.append(record)
        post_rows(record_batch)
        return total_results

    @staticmethod
    def delete_records(identifier: str, records: List[dict], table_name: str):
        total_results = {"failures": [],
                         "successes": []}

        def delete_row(row: dict):
            if not row:
                return
            id = f'{identifier}-{row["row_number"]}'
            del row["row_number"]
            data = {"row_data": row}
            client = PaperlessClient.get_instance()
            url = f"suppliers/public/custom_tables/{table_name}/row"
            result = custom_table_delete_row(client=client, data=data, url=url, identifier=id)

            # a 204 response indicates the delete was succesful, otherwise it is a failure
            if result != 204:
                total_results["failures"] += [row]
            else:
                total_results["successes"] += [row]

        for record in records:
            delete_row(record)
        return total_results

    @staticmethod
    def check_custom_table_exists(name: str, model: Model, id_fields: Union[str, List[str]] = []):
        try:
            CustomTable.get(name)
        except PaperlessNotFoundException:
            # generate new table if table not found
            ImportCustomTable.import_from_django_model(model, name, recreate=False, generate_table_data=False,
                                                       id_fields=id_fields)

    @staticmethod
    def check_custom_header_custom_table_exists(name: str, header_dict: dict, id_fields: Union[str, List[str]] = []):
        try:
            CustomTable.get(name)
        except PaperlessNotFoundException as e:
            logger.info(f"Table does not exist: {e}")
            ImportCustomTable.import_from_custom_dict(header_dict, name, recreate=False, generate_table_data=False,
                                                      id_fields=id_fields)

    @staticmethod
    def get_last_processed_date(identifier: str):
        """
        A function which, for a certain type of action (say "account_import"), gets the date out of a custom table for
        state storage and converts it to a datetime object

        @param identifier: The type of date you would want to access. For example, "purchased_component_import"
        @return: datetime object
        """
        try:
            integration_state_info = CustomTable.get('integration_state_info')
        except PaperlessNotFoundException:
            return pendulum.naive(year=1970, month=1, day=1)
        rows = integration_state_info['rows']
        for row in rows:
            if row['process_type'] == identifier:
                # we add a few min of buffer if trying to update at a very fast interval, possible that records can slip through
                dt = datetime.strptime(row['last_processed_date'], '%Y-%m-%d %H:%M:%S')
                dt_delta = timedelta(minutes=3)
                return dt - dt_delta
        return pendulum.naive(year=1970, month=1, day=1)

    @staticmethod
    def get_last_processed_date_sql(identifier: str):
        """
        Return a raw SQL query that returns the date for an action, converted to local time (relative to the
        SQL server).
        """
        date_to_search = ImportCustomTable.get_last_processed_date(identifier)
        to_search_adjusted_time_query = f"SELECT DATEADD(second, -DATEDIFF(second, getdate(), getutcdate()), " \
                                        f"'{date_to_search}')"
        return RawSQL(to_search_adjusted_time_query, [])

    @staticmethod
    def update_last_processed_date(identifier: str):
        """
        A function which, for a certain type of action (say "account_import"), updates the date out of a custom table for
        state storage

        @param identifier: The type of date you would want to update. For example, "purchased_component_import"
        @return: None
        """
        str_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        try:
            integration_state_info = CustomTable.get('integration_state_info')
        # if you do not find the table, import all
        except PaperlessNotFoundException:
            integration_state_info = None
            table_data = [dict(process_type=identifier, last_processed_date=str_date)]
        config = ImportCustomTable.assemble_config([["process_type", "string"], ["last_processed_date", "string"]])
        if integration_state_info:
            rows = integration_state_info['rows']
            found = False
            for row in rows:
                row.pop('row_number')
                if row['process_type'] == identifier:
                    found = True
                    row['last_processed_date'] = str_date
            if not found:
                rows.append(dict(process_type=identifier, last_processed_date=str_date))
            table_data = rows
        ImportCustomTable.upload_custom_table(config, table_data, 'integration_state_info')


class HexImportCustomTable(ImportCustomTable):
    """For integrations which use hex counts instead of dates - like MieTrak Pro"""

    @staticmethod
    def get_last_processed_hex_counter(identifier: str):
        """
        A function which, for a certain type of action (say "account_import"), gets the hex counter out of a custom
        table for state storage

        @param identifier: The type of hex counter you would want to access. For example, "purchased_component_import"
        @return: A hexadecimal string
        """
        try:
            integration_state_info = CustomTable.get('integration_state_info')
        except PaperlessNotFoundException:
            return '0x0000000000000000'
        rows = integration_state_info['rows']
        for row in rows:
            if row['process_type'] == identifier:
                # TODO - the get_last_processed_date method builds in a 3 minute buffer, do something similar here?
                #  Not obvious what buffer to use if so since the hex counter is global (?)
                hex_counter = row['last_processed_hex_counter']
                return hex_counter
        return '0x0000000000000000'

    @staticmethod
    def update_last_processed_hex_counter(identifier: str, hex_counter: str):
        """
        A function which, for a certain type of action (say "account_import"), updates the hex counter out of a custom
        table for state storage

        @param identifier: The type of hex counter you would want to access. For example, "purchased_component_import"
        @param hex_counter: The highest lastaccess value processed so far for this identifier.
        @return: None
        """
        try:
            integration_state_info = CustomTable.get('integration_state_info')
        # if you do not find the table, import all
        except PaperlessNotFoundException:
            integration_state_info = None
            table_data = [dict(process_type=identifier, last_processed_hex_counter=hex_counter)]
        config = ImportCustomTable.assemble_config([["process_type", "string"],
                                                    ["last_processed_hex_counter", "string"]])
        if integration_state_info:
            rows = integration_state_info['rows']
            found = False
            for row in rows:
                row.pop('row_number')
                if row['process_type'] == identifier:
                    found = True
                    row['last_processed_hex_counter'] = hex_counter
            if not found:
                rows.append(dict(process_type=identifier, last_processed_hex_counter=hex_counter))
            table_data = rows
        ImportCustomTable.upload_custom_table(config, table_data, 'integration_state_info')


class CustomTableFormat:

    _custom_table_name: str  # This is what will appear in paperless, and how the table will be referenced
    _primary_key: str  # This is the attribute alias

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

import sqlite3
from django.db import connections
from django.apps import apps
from baseintegration.utils import logger
import decimal


class SQLiteDBBase:
    def __init__(self, erp_name: str):
        self.database_name: str = "sql_database_copy.db"
        self.erp_name = erp_name
        self.sqlite_cursor = None
        self.sqlite_connection = None
        self.source_db_connection = None
        self.source_db_cursor = None
        self.chunk_size = 100000  # 100k chunks = ~85% of docker container memory usage
        self.index = 0
        self.total_rows = 0
        self.configure_db_connections()
        self.tables_and_pks = []

    def configure_db_connections(self):
        if self.sqlite_connection is None:
            logger.info("Configuring SQLite database connections.")
            self.sqlite_connection = sqlite3.connect(self.database_name, detect_types=sqlite3.PARSE_DECLTYPES)
            self.sqlite_cursor = self.sqlite_connection.cursor()

        if self.source_db_connection is None:
            logger.info(f"Configuring {self.erp_name} database connections.")
            self.source_db_connection = connections.all()[0]
            self.source_db_cursor = self.source_db_connection.cursor()

    def teardown_db_connections(self):
        self.sqlite_cursor = None
        self.sqlite_connection = None
        self.source_db_connection = None
        self.source_db_cursor = None


class DataManager(SQLiteDBBase):
    def select_data_in_chunks(self, table_name, pk_name, model=None):
        if model is None:
            model = apps.get_model(self.erp_name, str(table_name.replace("_", "")))
        self.teardown_db_connections()
        self.configure_db_connections()
        self.total_rows = model.objects.count()
        logger.info(f"{table_name} has {self.total_rows} rows.")
        dataset_exists = self.check_if_data_already_exists(model)

        if not dataset_exists:
            while self.index < self.total_rows:
                logger.info(f"Querying {self.index} <= row < {self.index + self.chunk_size}")
                try:
                    self.configure_db_connections()
                    self.sqlite_cursor.execute("pragma journal_mode=wal")
                    self.source_db_cursor.execute(
                        f"WITH Ops AS (SELECT *, ROW_NUMBER() OVER(ORDER BY {pk_name}) rownum FROM {table_name}) "
                        f"SELECT * FROM Ops WHERE rownum >= {self.index} AND rownum < {self.index + self.chunk_size}")
                    results: list = self.source_db_cursor.fetchall()
                except Exception as e:
                    logger.info(f"Failed to execute query. Tearing down DB connections. {e}")
                    self.teardown_db_connections()
                    continue

                self.index += self.chunk_size
                self.bulk_insert_data_into_sqlite_table(table_name, results)
        self.index = 0

    def check_if_data_already_exists(self, model):
        logger.info("Checking if SQLite table already exists.")
        try:
            total_sqlite_row_count = \
                model.objects.using('sqlite_copy').count()
            logger.info(f"Total SQLite row count = {total_sqlite_row_count}, total {self.erp_name} row count = "
                        f"{self.total_rows}")
            if self.total_rows == total_sqlite_row_count:
                logger.info(f"SQLite database already contains all {self.erp_name} data.")
                return True
            elif self.total_rows > total_sqlite_row_count > 0:
                logger.info("Rows are missing from the SQLite database. Attempting to pick up where we left off.")
                self.index = total_sqlite_row_count + 1
                return False
            else:
                logger.info("No data exists in SQLite database... Attempting to SELECT and INSERT data.")
                return False
        except Exception as e:
            logger.info(f"Could not query SQLite table. {e}")
            return False

    def bulk_insert_data_into_sqlite_table(self, table_name: str, query_results: list):
        placeholders = self.get_placeholder_length(query_results[0])
        insert_list = []
        for result in query_results:
            result = self.type_cast_sql_server_data(result)
            insert_list.append(result[:-1])
        # Batch insert will always be the same size as SELECT statement specification
        try:
            query_string = f"INSERT INTO {table_name} VALUES ({placeholders})"
            self.sqlite_cursor.executemany(query_string, insert_list)
            self.sqlite_connection.commit()
            logger.info(f"Successfully inserted batch of {len(query_results)} rows.")
        except Exception as e:
            logger.info(f"Could not bulk insert {len(query_results)} rows. {e}")

    def get_placeholder_length(self, sql_row):
        placeholders = ""
        for item in range(0, len(sql_row) - 1):
            placeholders += "?,"
        return placeholders[:-1]

    def type_cast_sql_server_data(self, sql_row):
        clean_row = []
        for value in sql_row:
            if isinstance(value, (str, int, float)):
                clean_row.append(value)
            elif isinstance(value, decimal.Decimal):
                clean_row.append(float(value))
            elif isinstance(value, bool):
                clean_row.append(int(value))
            elif value is None:
                clean_row.append(value)
            else:
                clean_row.append(str(value))
        return clean_row

    def drop_list_of_sqlite_tables(self, tables_list: list):
        self.configure_db_connections()
        for table in tables_list:
            try:
                self.sqlite_cursor.execute(f"DROP TABLE IF EXISTS {str(table)}")
                self.sqlite_cursor.commit()
                logger.info(f"Dropped table {table}.")
            except Exception as e:
                logger.info(f"Could not drop table {table}... {e}")


class SQLiteDBGenerator(SQLiteDBBase):
    def create_sqlite_table_from_model(self, model):
        table_name = model._meta.db_table
        pk_field_name = model._meta.pk.column
        self.tables_and_pks.append((model, table_name, pk_field_name))
        return self.create_sqlite_table_from_sql_server_schema(table_name, pk_field_name)

    def create_sqlite_table_from_sql_server_schema(
            self,
            sql_server_table_name: str,
            pk_field_name: str,  # leave blank for views
            fk_field_name: str = None,
            fk_table_name: str = None,
            fk_table_fk_id: str = None,
    ):
        logger.info(f"Attempting to create SQLite table schema from {sql_server_table_name} table data...")
        self.configure_db_connections()
        example_data = self.source_db_cursor.execute(f"SELECT TOP 1 * FROM {sql_server_table_name}").fetchall()[0]  # noqa: F841
        header_data = self.source_db_cursor.description

        # Assemble string to assign table headers
        header_string = ""
        for header in header_data:
            header_name = str(header[0])
            type_code = str(header[1])
            sqlite_data_type = self.get_data_type(type_code)
            if header_name == pk_field_name:
                header_string += f"[{header_name}] {sqlite_data_type} PRIMARY KEY,"
            else:
                header_string += f"[{header_name}] {sqlite_data_type},"
        header_string = header_string[:-1]

        # Assemble string to create table and associate PK/FK relationships if present
        query_string = f"CREATE TABLE {sql_server_table_name} ({header_string}"
        if fk_field_name and fk_table_name and fk_table_fk_id:
            query_string += f",FOREIGN KEY ({fk_field_name}) REFERENCES {fk_table_name}({fk_table_fk_id})"
        query_string += ")"

        logger.info(f"Attempting to execute query:\n{query_string}")
        try:
            self.sqlite_cursor.execute(query_string)
        except Exception as e:
            logger.info(f"Could not create new SQLite table: {e}")

    def get_data_type(self, type_code):
        if type_code == "<class 'int'>" or type_code == "<class 'bool'>":
            return "INTEGER"
        elif type_code == "<class 'float'>" or type_code == "<class 'decimal.Decimal'>":
            return "REAL"
        else:
            return "TEXT"

    def create_sqlite_index(self, index_name, table_name, column_list):
        logger.info("Creating index.")
        self.configure_db_connections()
        query_string = f"CREATE INDEX {index_name} ON {table_name}({column_list})"
        try:
            self.sqlite_cursor.execute(query_string)
        except Exception as e:
            logger.info(f"Could not index:\n{query_string}\nError: {e}")

    def create_sqlite_index_from_fields(self, *model_fields):
        fields = [f.field for f in model_fields]
        model = fields[0].model
        table_name = model._meta.db_table
        column_list = [field.column for field in fields]
        columns_str = ", ".join(column_list)
        index_name = f"{table_name}_{'_'.join(column_list)}"
        return self.create_sqlite_index(index_name, table_name, columns_str)

    def copy_data_to_sqlite(self):
        data_manager = DataManager(self.erp_name)
        for model, table_name, pk_name in self.tables_and_pks:
            data_manager.select_data_in_chunks(table_name, pk_name, model)

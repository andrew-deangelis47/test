from dataclasses import dataclass, field
from typing import List, Union

from baseintegration.datamigration import logger
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from baseintegration.importer.material_importer import MaterialImporter
from baseintegration.importer.repeat_part_importer import RepeatPartImporter
from baseintegration.importer.work_center_importer import WorkCenterImporter
from baseintegration.utils.custom_table import HexImportCustomTable, ImportCustomTable
from baseintegration.utils.repeat_work_objects import Part, Header, MethodOfManufacture
from m2m.importer.processors.materials import M2MMaterialImporterProcessor, M2MMaterialBulkImportProcessor, \
    M2MMaterialBulkPlaceholder
from m2m.importer.processors.accounts import AccountImportProcessor
from m2m.importer.processors.purchased_component import M2MPurchasedComponentImportProcessor, \
    M2MPurchasedComponentBulkImportProcessor, M2MPurchasedComponentBulkPlaceholder
from m2m.importer.processors.work_centers import M2MWorkCenterImportProcessor, M2MWorkCenterBulkPlaceholder, \
    M2MWorkCenterBulkImportProcessor
from m2m.configuration import ERPDBConfigFactory, M2MConfiguration
from m2m.importer.repeat_work_processors.header import HeaderProcessor
from m2m.importer.repeat_work_processors.method_of_manufacture import MethodOfManufactureProcessor
from m2m.importer.repeat_work_processors.repeat_part import RepeatPartProcessor
from m2m.models import Slcdpmx, Inmastx, Inwork
from django.db import connection

from m2m.utils.repeat_work_utils import create_all_sqlite_tables_if_not_exists, insert_data_into_all_sqlite_tables, \
    create_indexes_on_all_sqlite_tables


class BaseM2MListener:
    _m2m_config = M2MConfiguration()

    def __init__(self, integration, m2m_config):
        self._integration = integration
        self._m2m_config = m2m_config


class M2MAccountListener:
    identifier = "import_account"

    def __init__(self, integration):
        self._integration = integration

    def get_new(self, bulk=False):
        logger.info("Processing: Accounts")
        cursor = connection.cursor()
        try:
            last_processed_hex_counter = HexImportCustomTable.get_last_processed_hex_counter(self.identifier)

            account_query = f"SELECT fcustno, " \
                            f"(SELECT MAX(rev_number) " \
                            f"FROM(VALUES(ac.timestamp_column), (addr.timestamp_column), (con.timestamp_column)) " \
                            f"AS UpdateDate(rev_number)) " \
                            f"AS rev_number " \
                            f"FROM slcdpmx as ac " \
                            f"LEFT JOIN syaddr as addr ON ac.fcustno = addr.fcaliaskey " \
                            f"LEFT JOIN syphon as con ON ac.fcustno = con.fcsourceid " \
                            f"WHERE fcstatus != 'N' " \
                            f"AND(ac.timestamp_column > CAST({last_processed_hex_counter} as timestamp) " \
                            f"OR addr.timestamp_column > CAST({last_processed_hex_counter} as timestamp) " \
                            f"OR con.timestamp_column > CAST({last_processed_hex_counter} as timestamp)) " \
                            f"ORDER BY rev_number ASC"
            cursor.execute(account_query)
            account_query_set = cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
        a_list = []
        for item in account_query_set:
            a_list.append(item[0])
        final_ordered_list = list(dict.fromkeys(a_list))
        logger.info(f'Accounts to update {len(final_ordered_list)}')
        return final_ordered_list


class M2MAccountImporter(AccountImporter):
    """An integration config specific to m2m"""
    m2m_config = M2MConfiguration()

    def _setup_erp_config(self):
        self.erp_config, self.m2m_config = ERPDBConfigFactory.create_configs(self._integration)

    def _register_default_processors(self):
        self.register_processor(Slcdpmx, AccountImportProcessor)

    def _register_listener(self):
        self.listener = M2MAccountListener(self._integration)

    def _process_account(self, account_id: str):
        self._setup_erp_config()
        logger.info(f"Processing Account: {str(account_id)}")
        with self.process_resource(Slcdpmx, account_id, self.m2m_config) as last_hex_counter:
            HexImportCustomTable.update_last_processed_hex_counter(M2MAccountListener.identifier, last_hex_counter)
            logger.info(f"Processed Account: {str(account_id)}")
            return True


class M2MPurchasedComponentListener(BaseM2MListener):
    identifier = "import_purchased_component"

    def get_new(self, bulk=False):
        cursor = connection.cursor()
        try:
            if bulk:
                last_processed_hex_counter = last_hex_counter = '0x0000000000000000'
            else:
                last_processed_hex_counter = last_hex_counter = HexImportCustomTable.get_last_processed_hex_counter(
                    self.identifier)
            purchase_condition = "fcpurchase = 'Y'"
            if self._m2m_config.purchase_condition:
                purchase_condition = self._m2m_config.purchase_condition
            purchase_component_query = f"SELECT fpartno, timestamp_column from inmastx " \
                                       f"WHERE {purchase_condition} " \
                                       f"AND timestamp_column > CAST({last_processed_hex_counter} as timestamp) " \
                                       f"ORDER BY timestamp_column ASC"
            cursor.execute(purchase_component_query)
            purchase_component_query_set = cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
        p_list = []
        for item in purchase_component_query_set:
            p_list.append(item[0])
            if last_hex_counter < f'0x{item[1].hex()}':
                last_hex_counter = f'0x{item[1].hex()}'
        HexImportCustomTable.update_last_processed_hex_counter(self.identifier, last_hex_counter)
        logger.info(f'Purchase components to update {len(p_list)}')
        return p_list


class M2MPurchasedComponentImporter(PurchasedComponentImporter):
    """An integration config specific to m2m"""
    _m2m_config = M2MConfiguration()

    def _setup_erp_config(self):
        self.erp_config, self._m2m_config = ERPDBConfigFactory.create_configs(self._integration)

    def _register_listener(self):
        self.listener = M2MPurchasedComponentListener(self._integration, self._m2m_config)
        logger.info("M2M purchased component listener was registered")

    def _register_default_processors(self):
        self.register_processor(Inmastx, M2MPurchasedComponentImportProcessor)
        self.register_processor(M2MPurchasedComponentBulkPlaceholder, M2MPurchasedComponentBulkImportProcessor)

    def _process_purchased_component(self, purchased_component_id: str):
        with self.process_resource(Inmastx, purchased_component_id) as success:
            logger.info(f"Processed purchased component: {str(purchased_component_id)}")
            return success

    def _bulk_process_purchased_component(self, purchased_component_ids: List[str]):
        with self.process_resource(M2MPurchasedComponentBulkPlaceholder, purchased_component_ids) as success:
            logger.info(f"Bulk processed purchased component: {len(purchased_component_ids)}")
            return success


class M2MMaterialListener(BaseM2MListener):
    identifier = "import_material"

    def get_new(self, bulk=False):
        m_cursor = connection.cursor()
        i_list = []
        try:
            if bulk:
                last_processed_hex_counter = last_hex_counter = '0x0000000000000000'
            else:
                last_processed_hex_counter = last_hex_counter = HexImportCustomTable.get_last_processed_hex_counter(
                    self.identifier)
            logger.info(f'last processed hex stamp {last_processed_hex_counter}')
            material_condition = None
            if self._m2m_config.material_condition:
                material_condition = self._m2m_config.material_condition
            if material_condition is None:
                logger.info('Material conditional not set bailing')
                return i_list
            material_query = f"SELECT fpartno, timestamp_column from inmastx " \
                             f"WHERE {material_condition} AND timestamp_column > CAST({last_processed_hex_counter} as timestamp) " \
                             f"ORDER BY timestamp_column ASC"
            m_cursor.execute(material_query)
            material_query_set = m_cursor.fetchall()
        finally:
            m_cursor.close()
            connection.close()
        for item in material_query_set:
            i_list.append(item[0])
            if last_hex_counter < f'0x{item[1].hex()}':
                last_hex_counter = f'0x{item[1].hex()}'
        HexImportCustomTable.update_last_processed_hex_counter(self.identifier, last_hex_counter)
        count = len(i_list)
        logger.info(f'Raw Materials to update {count}')
        return i_list


class M2MMaterialImporter(MaterialImporter):
    """An integration config specific to m2m"""
    _m2m_config = M2MConfiguration()
    _is_for_unique_key = ['fpartno', 'frev']

    def _setup_erp_config(self):
        self.erp_config, self._m2m_config = ERPDBConfigFactory.create_configs(self._integration)

    def _register_listener(self):
        self.listener = M2MMaterialListener(self._integration, self._m2m_config)
        logger.info("M2M material listener was registered")

    def _register_default_processors(self):
        self.register_processor(Inmastx, M2MMaterialImporterProcessor)
        self.register_processor(M2MMaterialBulkPlaceholder, M2MMaterialBulkImportProcessor)

    """
    This method is overridden to from the base class
    :param material_id: This will be the values of the identity_column in the M2M DB or RESYNC-{hex stamp}
    """

    def _process_material(self, material_id: str):
        with self.process_resource(Inmastx, material_id) as success:
            logger.info(f"Processed raw materials: {material_id}")
            return success

    def _bulk_process_material(self, material_ids: List[str]):
        with self.process_resource(M2MMaterialBulkPlaceholder, material_ids) as success:
            logger.info(f"Bulk processed purchased component: {len(material_ids)}")
            return success

    def check_custom_table_exists(self):
        cost_name = "fstdcost"
        if self._m2m_config.material_use_total_cost:
            cost_name = "f2totcost"
        self.header_dict = {
            'fpartno': '',
            'frev': '',
            'fcudrev': '',
            'fdescript': '',
            f'{cost_name}': 0.000,
            'fmeasure': '',
            'frevdt': '',
            'identity_column': 0,
        }
        if self._m2m_config.material_add_group_code:
            self.header_dict['fgroup'] = ''
        if self._m2m_config.material_add_product_class:
            self.header_dict['fprodcl'] = ''

        name = M2MMaterialImporterProcessor.table_name
        ImportCustomTable.check_custom_header_custom_table_exists(name, self.header_dict, self._is_for_unique_key)


class M2MWorkCenterListener(BaseM2MListener):
    identifier = "import_work_center"

    def get_new(self, bulk=False):
        m_cursor = connection.cursor()
        w_list = []
        try:
            if bulk:
                last_processed_hex_counter = last_hex_counter = '0x0000000000000000'
            else:
                last_processed_hex_counter = last_hex_counter = \
                    HexImportCustomTable.get_last_processed_hex_counter(self.identifier)

            w_query = f"SELECT fcpro_id, timestamp_column FROM Inwork " \
                      f"WHERE timestamp_column > CAST({last_processed_hex_counter} as timestamp) " \
                      f"ORDER BY timestamp_column ASC"
            m_cursor.execute(w_query)
            w_query_set = m_cursor.fetchall()

            op_query = f"SELECT fcpro_id, timestamp_column FROM Inopds " \
                       f"WHERE timestamp_column > CAST({last_processed_hex_counter} as timestamp) " \
                       f"ORDER BY timestamp_column ASC"
            m_cursor.execute(op_query)
            op_query_set = m_cursor.fetchall()
        finally:
            m_cursor.close()
            connection.close()
        for item in w_query_set:
            w_list.append(f'{item[0]}'.strip())
            if last_hex_counter < f'0x{item[1].hex()}':
                last_hex_counter = f'0x{item[1].hex()}'
        for item in op_query_set:
            wc = f'{item[0]}'.strip()
            if wc not in w_list:
                w_list.append(wc)
            if last_hex_counter < f'0x{item[1].hex()}':
                last_hex_counter = f'0x{item[1].hex()}'
        logger.info(f'Workcenter and Ops to update {len(w_list)}')
        HexImportCustomTable.update_last_processed_hex_counter(M2MMaterialListener.identifier, last_hex_counter)
        return w_list


class M2MWorkCenterImporter(WorkCenterImporter):
    """An integration config specific to m2m"""
    op_header_dict = {}
    w_header_dict = {}
    _m2m_config = M2MConfiguration()

    def _setup_erp_config(self):
        self.erp_config, self._m2m_config = ERPDBConfigFactory.create_configs(self._integration)

    def _register_listener(self):
        self.listener = M2MWorkCenterListener(self._integration, self._m2m_config)
        logger.info("M2M work center listener was registered")

    def _register_default_processors(self):
        self.register_processor(Inwork, M2MWorkCenterImportProcessor)
        self.register_processor(M2MWorkCenterBulkPlaceholder, M2MWorkCenterBulkImportProcessor)

    def check_custom_table_exists(self):
        self.w_header_dict = {
            'fnavgwkhrs': 0.0,
            'fcpro_id': '',
            'fcpro_name': '',
            'fccomments': '',
            'fdept': '',
            'flabcost': 0.0,
            'fnavgque': 0.0,
            'flschedule': '',
            'fnmax1': 0,
            'fnmax2': 0,
            'fnmax3': 0,
            'fnmaxque': 0.0,
            'fnpctutil': 0.0,
            'fnqueallow': 0.0,
            'fnstd1': 0,
            'fnstd2': 0,
            'fnstd3': 0,
            'fnstd_prod': 0.0,
            'fnstd_set': 0.0,
            'fnsumdur': 0.0,
            'fovrhdcost': 0.0,
            'fscheduled': '',
            'fspandays': 0,
            'fnpque': 0.0,
            'flconstrnt': '',
            'identity_column': 0,
            'fac': '',
            'fcstdormax': '',
            'fndbrmod': 0,
            'fnloadcapc': 0.0,
            'fnmaxcapload': 0.0,
            'flaltset': '',
            'fcsyncmisc': '',
            'queuehrs': 0.0,
            'constbuff': 0.0,
            'resgroup': '',
            'flbflabor': '',
            'cycleunits': 0.0,
            'simopstype': '',
            'size': 0.0,
            'canbreak': '',
            'sizeum': '',
            'timefence': 0,
            'fcgroup': '',
            'fracsimops': ''
        }

        w_name = M2MWorkCenterBulkImportProcessor.w_table_name
        ImportCustomTable.check_custom_header_custom_table_exists(w_name, self.w_header_dict, ['fcpro_id'])

        self.op_header_dict = {
            'fdescnum': '',
            'fcpro_id': '',
            'fnstd_prod': 0.0,
            'fnstd_set': 0.0,
            'identity_column': 0,
            'fopmemo': '',
            'fac': '',
        }

        op_name = M2MWorkCenterBulkImportProcessor.op_table_name
        ImportCustomTable.check_custom_header_custom_table_exists(op_name, self.op_header_dict, ['fcpro_id', 'fdescnum'])
        return True

    def _process_work_center(self, work_center_id: str):  # noqa: C901
        with self.process_resource(Inwork, work_center_id) as result:
            logger.info("Processed work center")
            return result

    def _bulk_process_work_center(self, work_center_ids: List[str]):
        with self.process_resource(M2MWorkCenterBulkPlaceholder, work_center_ids) as result:
            logger.info("Processed bulk work center")
            return result


@dataclass
class TableMonitor:
    table_name: str
    depends_on: List['ChildTableMonitor'] = field(default_factory=list)
    filters: List[str] = field(default_factory=list)
    extra_joins: str = ""


@dataclass
class RootTableMonitor(TableMonitor):
    id_columns: tuple[str, str] = ("", "")


@dataclass
class ChildTableMonitor(TableMonitor):
    relates_to_parent_on: Union[str, tuple] = ""


class M2MRepeatWorkImportListener(BaseM2MListener):

    def __init__(self, integration, m2m_config):
        super().__init__(integration, m2m_config)
        self.identifier = "import_repeat_part"
        self.total_part_objects = 0
        logger.info("M2M repeat import listener was instantiated")

    def get_new(self, bulk=False, date_to_search=None):
        ids = set()
        logger.info("Checking for new repeat work")

        m_cursor = connection.cursor()
        query_set = []
        try:
            if bulk:
                last_processed_hex_counter = last_hex_counter = '0x0000000000000000'
                create_all_sqlite_tables_if_not_exists()
                insert_data_into_all_sqlite_tables()
                create_indexes_on_all_sqlite_tables()
            else:
                last_processed_hex_counter = last_hex_counter = HexImportCustomTable.get_last_processed_hex_counter(
                    self.identifier)

            logger.info(f'last processed hex stamp {last_processed_hex_counter}')

            tables_to_monitor = [
                RootTableMonitor(table_name="Inmastx", id_columns=("fpartno", "frev")),
                RootTableMonitor(table_name="Qtitem", id_columns=("fpartno", "fpartrev"), depends_on=[
                    ChildTableMonitor(table_name="Qtdbom", relates_to_parent_on=("fquoteno", "finumber")),
                    ChildTableMonitor(table_name="Qtdbom", relates_to_parent_on=("fquoteno", "finumber")),
                    ChildTableMonitor(table_name="Qtpest", relates_to_parent_on=("fquoteno", "finumber")),
                ]),
                RootTableMonitor(table_name="Jomast", id_columns=("fpartno", "fpartrev"),
                                 filters=["Jomast.ftype='C'"], depends_on=[
                    ChildTableMonitor(table_name="Jodbom", relates_to_parent_on="fjobno"),
                    ChildTableMonitor(table_name="Jodrtg", relates_to_parent_on="fjobno"),
                ]),
                RootTableMonitor(table_name="Qtdbom", id_columns=("fbompart", "fbomrev")),
                RootTableMonitor(table_name="Jodbom", id_columns=("fbompart", "fbomrev"),
                                 extra_joins="INNER JOIN Jomast ON Jodbom.fjobno = Jomast.fjobno",
                                 filters=["Jomast.ftype='C'"], depends_on=[
                    ChildTableMonitor(table_name="Jomast", relates_to_parent_on="fjobno", filters=["Jomast.ftype='C'"])
                ]),
            ]

            queries = self._get_queries_from_table_monitors(tables_to_monitor, last_processed_hex_counter)
            for query in queries:
                m_cursor.execute(query)
                query_set.extend(m_cursor.fetchall())
        finally:
            m_cursor.close()
            connection.close()
        for item in query_set:
            ids.add((item[0], item[1]))
            if last_hex_counter < f'0x{item[2].hex()}':
                last_hex_counter = f'0x{item[2].hex()}'
        HexImportCustomTable.update_last_processed_hex_counter(self.identifier, last_hex_counter)
        self.total_part_objects = len(ids)
        logger.info(f"Found {self.total_part_objects} records to update")
        return ids

    def _process_monitor(
            self, monitor: TableMonitor, root_monitor: RootTableMonitor, last_processed_hex_counter, joins: str = ""):
        queries = []
        selected_columns = f"{root_monitor.table_name}.{root_monitor.id_columns[0]}, " \
                           f"{root_monitor.table_name}.{root_monitor.id_columns[1]}"
        filters = [f"{monitor.table_name}.timestamp_column > CAST({last_processed_hex_counter} as timestamp)"]
        filters += monitor.filters
        filters_string = " AND ".join(filters)
        all_joins = f"{joins} {monitor.extra_joins}"
        query = f"SELECT {selected_columns}, {monitor.table_name}.timestamp_column " \
                f"FROM {root_monitor.table_name} {all_joins} WHERE {filters_string}"
        queries.append(query)
        for child_monitor in monitor.depends_on:
            join_conditions = []
            relates_to_parent_on = child_monitor.relates_to_parent_on
            if not isinstance(relates_to_parent_on, tuple):
                relates_to_parent_on = tuple([relates_to_parent_on])
            for related_field in relates_to_parent_on:
                join_condition = f"{child_monitor.table_name}.{related_field} = {monitor.table_name}.{related_field}"
                join_conditions.append(join_condition)
            join_conditions_string = " AND ".join(join_conditions)
            child_joins = f"{joins} INNER JOIN {child_monitor.table_name} ON {join_conditions_string}"
            queries += self._process_monitor(child_monitor, root_monitor, last_processed_hex_counter, child_joins)
        return queries

    def _get_queries_from_table_monitors(self, table_monitors: List[RootTableMonitor], last_processed_hex_counter):
        """
        Parses the list of table monitors into a series of queries that return a list of updated entries.
        """
        all_queries = []
        for monitor in table_monitors:
            all_queries.extend(self._process_monitor(monitor, monitor, last_processed_hex_counter))
        return all_queries


class M2MRepeatPartImporter(RepeatPartImporter):
    split_id = True
    _m2m_config = M2MConfiguration()

    def _setup_erp_config(self):
        self.erp_config, self._m2m_config = ERPDBConfigFactory.create_configs(self._integration)

    def _register_listener(self):
        self.listener = M2MRepeatWorkImportListener(self._integration, self._m2m_config)
        logger.info("M2M repeat part listener was registered")

    def _register_default_processors(self):
        self.register_processor(Part, RepeatPartProcessor)
        self.register_processor(Header, HeaderProcessor)
        self.register_processor(MethodOfManufacture, MethodOfManufactureProcessor)
        logger.info('Registered all repeat part processors.')

    def _process_repeat_part(self, repeat_part_id: Union[str, tuple[str, str]], create_child_parts: bool = False,
                             is_root: bool = True):
        logger.info(f"Attempting to process {str(repeat_part_id)}")
        self.total_parts_processed += 1

        if repeat_part_id in self.processed_children_list:
            logger.info(
                f"Part id: {repeat_part_id} matches an existing part number that has already been processed."
                f" Skipping this component to prevent infinite loop."
            )
        else:
            self.processed_children_list.append(repeat_part_id)
            with self.process_resource(Part, repeat_part_id) as (repeat_part, part_data):
                pass
            with self.process_resource(MethodOfManufacture, repeat_part, part_data, create_child_parts) \
                    as methods_of_manufacture:
                pass
            with self.process_resource(Header, repeat_part, part_data, methods_of_manufacture) as repeat_part:
                pass

            repeat_part_json = repeat_part.to_json()
            self.post_repeat_part(repeat_part_json)

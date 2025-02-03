from typing import List

from baseintegration.datamigration import logger
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.importer.material_importer import MaterialImporter
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from paperless.objects.customers import Account
from paperless.objects.components import PurchasedComponent
from paperless.objects.components import Material

from baseintegration.importer.repeat_part_importer import RepeatPartImporter
from inforsyteline.importer.configuration import RepeatPartImportConfig
from baseintegration.utils.repeat_work_objects import Part, MethodOfManufacture, Header
from inforsyteline.importer.processors.account import AccountImportProcessor
from inforsyteline.importer.processors.material import MaterialImportProcessor, MaterialBulkPlaceholder, \
    MaterialBulkImportProcessor
from inforsyteline.importer.processors.purchased_component import PurchasedComponentImportProcessor, \
    PurchasedComponentBulkImportProcessor, PurchasedComponentBulkPlaceholder
from inforsyteline.importer.repeat_work_processors.header import HeaderProcessor
from inforsyteline.importer.repeat_work_processors.method_of_manufacture import MethodOfManufactureProcessor
from inforsyteline.importer.repeat_work_processors.repeat_part import RepeatPartProcessor
from inforsyteline.importer.repeat_work_utils import create_all_sqlite_tables_if_not_exists, \
    create_indexes_on_all_sqlite_tables
from inforsyteline.models import CustomerMst, ItemMst, JobMst
from baseintegration.utils.custom_table import ImportCustomTable
from baseintegration.utils import get_last_action_datetime_sql, get_last_action_datetime_value

from django.db import connection


class InforSytelineAccountImportListener:

    def __init__(self, integration):
        self.identifier = "import_account"
        self._integration = integration
        logger.info("Infor Syteline account import listener was instantiated")

    def get_new(self, bulk=False):
        customer_codes = set()
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        updated_customers_query_set = CustomerMst.objects.filter(recorddate__gt=date_to_search)

        for customer_code in updated_customers_query_set.values_list('cust_num', flat=True):
            customer_codes.add(str(customer_code).replace(" ", ""))

        logger.info(f"Found {len(customer_codes)} records to update")
        return customer_codes


class InforSytelineAccountImporter(AccountImporter):

    def _register_listener(self):
        self.listener = InforSytelineAccountImportListener(self._integration)
        logger.info("Infor Syteline account listener was registered")

    def _register_default_processors(self):
        self.register_processor(Account, AccountImportProcessor)

    def _process_account(self, account_id: str):  # noqa: C901
        logger.info(f"Processing account with id {account_id}")
        with self.process_resource(Account, account_id):
            logger.info(f"Processed account {str(account_id)}")


class InforSytelineMaterialImportListener:

    def __init__(self, integration):
        self.identifier = "import_material"
        self._integration = integration
        logger.info("Infor Syteline material import listener was instantiated")

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        updated_query_set = self.get_query_set(date_to_search)
        logger.info(f"Found {str(updated_query_set.count())} records to update")
        return updated_query_set.values_list('item', flat=True)

    def get_query_set(self, date_to_search):
        codes_to_include = self._integration.config_yaml["Importers"]["materials"].get("codes_to_include", [])
        updated_query_set = ItemMst.objects.filter(product_code__in=codes_to_include).filter(recorddate__gt=date_to_search)
        return updated_query_set


class InforSytelineMaterialImporter(MaterialImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "materials"
        else:
            self.table_name = "syteline_materials"

    def _register_listener(self):
        self.listener = InforSytelineMaterialImportListener(self._integration)
        logger.info("Infor Syteline material listener was registered")

    def check_custom_table_exists(self):
        logger.info("We're creating a dictionary.")
        self.header_dict = {
            'Item': "N/A",
            'Description': "N/A",
            'revision': "N/A",
            'ecn': "0",
            'buyer': "N/A",
            'stocked': 0,
            'u_m': "ea",
            'type': "material",
            'product_code': '3000',
            'abc_code': 'A',
            'cost_type': 'Actual',
            'cost_method': 'Average',
            'unit_cost': 0.0,
            'current_unit_cost': 0.0,
            'lot_size': 1,
            'unit_weight': 0,
            'weight_units': "LB"
        }
        return ImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict, "Item")

    def _register_default_processors(self):
        self.register_processor(Material, MaterialImportProcessor)
        self.register_processor(MaterialBulkPlaceholder, MaterialBulkImportProcessor)

    def _process_material(self, material_id: str):  # noqa: C901
        with self.process_resource(Material, material_id):
            logger.info(f"Processed material {str(material_id)}")

    def _bulk_process_material(self, material_ids: List[str]):
        with self.process_resource(MaterialBulkPlaceholder, material_ids) as success:
            logger.info(f"Bulk processed {len(material_ids)} materials")
            return success


class InforSytelinePurchasedComponentListener:

    def __init__(self, integration):
        self.identifier = "import_purchased_component"
        self._integration = integration
        logger.info("Infor syteline purchased component import listener was instantiated")

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        updated_query_set = self.get_query_set(date_to_search)
        logger.info(f"Found {str(updated_query_set.count())} records to update")
        return updated_query_set.values_list('item', flat=True)

    def get_query_set(self, date_to_search):
        codes_to_include = self._integration.config_yaml["Importers"]["purchased_components"].get("codes_to_include", [])
        updated_query_set = ItemMst.objects.filter(product_code__in=codes_to_include).filter(recorddate__gt=date_to_search)
        return updated_query_set


class InforSytelinePurchasedComponentImporter(PurchasedComponentImporter):

    def _register_listener(self):
        self.listener = InforSytelinePurchasedComponentListener(self._integration)
        logger.info("Infor Syteline purchased component listener was registered")

    def _register_default_processors(self):
        self.register_processor(PurchasedComponent, PurchasedComponentImportProcessor)
        self.register_processor(PurchasedComponentBulkPlaceholder, PurchasedComponentBulkImportProcessor)

    def _process_purchased_component(self, purchased_component_id: str):  # noqa: C901
        with self.process_resource(PurchasedComponent, purchased_component_id):
            logger.info(f"Processed purchased component {str(purchased_component_id)}")

    def _bulk_process_purchased_component(self, purchased_component_ids: List[str]):
        with self.process_resource(PurchasedComponentBulkPlaceholder, purchased_component_ids) as success:
            logger.info(f"Bulk processed {len(purchased_component_ids)} purchased components")
            return success


class InforSytelineRepeatWorkImportListener:
    def __init__(self, integration):
        self.identifier = "import_repeat_part"
        self._integration = integration
        self.total_part_objects = 0
        logger.info("Infor Syteline repeat import listener was instantiated")

    def get_new(self, bulk=False, date_to_search=None):
        if bulk:
            create_all_sqlite_tables_if_not_exists()
            create_indexes_on_all_sqlite_tables()
        if not date_to_search:
            date_to_search = get_last_action_datetime_value(
                self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        new_items_list = self.get_query_set(date_to_search)
        logger.info(f"Found {len(new_items_list)} records to update")
        return new_items_list

    def get_query_set(self, date_to_search) -> set[str]:
        items = set()

        # get updated items
        updated_items = ItemMst.objects.filter(recorddate__gt=date_to_search).values_list('item', flat=True)
        items.update(updated_items)

        # get items of updated jobs
        updated_items = JobMst.objects.filter(recorddate__gt=date_to_search).values_list('item', flat=True)
        items.update(updated_items)

        with connection.cursor() as cursor:
            # get items of updated job materials
            materials_query = "SELECT DISTINCT Job_Mst.item FROM Jobmatl_Mst " \
                              "INNER JOIN Job_Mst ON Job_Mst.job = Jobmatl_Mst.job " \
                              f"WHERE Jobmatl_Mst.RecordDate > '{date_to_search}'"
            cursor.execute(materials_query)
            updated_items = [job[0] for job in cursor.fetchall()]
            items.update(updated_items)

            # get items of updated job operations
            operations_query = "SELECT DISTINCT Job_Mst.item FROM Jobroute_Mst " \
                               "INNER JOIN Job_Mst ON Job_Mst.job = Jobroute_Mst.job " \
                               f"WHERE Jobroute_Mst.RecordDate > '{date_to_search}'"
            cursor.execute(operations_query)
            updated_items = [job[0] for job in cursor.fetchall()]
            items.update(updated_items)

            # get items of updated customer orders (i.e. quotes)
            estimate_lines_query = "SELECT DISTINCT Coitem_Mst.item FROM Coitem_Mst " \
                                   "INNER JOIN Co_Mst ON Co_Mst.co_num = Coitem_Mst.co_num " \
                                   f"WHERE Co_Mst.type = 'E' AND Coitem_Mst.RecordDate > '{date_to_search}'"
            cursor.execute(estimate_lines_query)
            updated_items = [job[0] for job in cursor.fetchall()]
            items.update(updated_items)

        return items


class InforSytelineRepeatPartImporter(RepeatPartImporter):
    def _register_listener(self):
        self.listener = InforSytelineRepeatWorkImportListener(self._integration)
        logger.info("Infor Syteline repeat part listener was registered")

    def _setup_erp_config(self):
        self.erp_config = RepeatPartImportConfig(self._integration.config_yaml)

    def _register_default_processors(self):
        self.register_processor(Part, RepeatPartProcessor)
        self.register_processor(Header, HeaderProcessor)
        self.register_processor(MethodOfManufacture, MethodOfManufactureProcessor)
        logger.info('Registered all repeat part processors.')

    def _process_repeat_part(self, repeat_part_id: str, create_child_parts: bool = False, is_root: bool = True):
        logger.info(f"Attempting to process {str(repeat_part_id)}")
        self.total_parts_processed += 1

        if repeat_part_id in self.processed_children_list:
            logger.info(
                f"Part id: {repeat_part_id} matches an existing part number that has already been processed."
                f" Skipping this component to prevent infinite loop."
            )
        else:
            self.processed_children_list.append(repeat_part_id)
            with self.process_resource(Part, repeat_part_id) as repeat_part:
                pass
            with self.process_resource(MethodOfManufacture, repeat_part, create_child_parts) as methods_of_manufacture:
                pass
            with self.process_resource(Header, repeat_part, methods_of_manufacture) as repeat_part:
                pass

            repeat_part_json = repeat_part.to_json()
            self.post_repeat_part(repeat_part_json)

from typing import List

from baseintegration.importer.material_importer import MaterialImporter
from baseintegration.importer.custom_table_record_importer import CustomTableRecordImporter
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from baseintegration.importer.vendor_importer import VendorImporter
from baseintegration.importer.work_center_importer import WorkCenterImporter
from globalshop.importer.processors.purchased_component import GlobalShopPurchasedComponentImportProcessor,\
    GlobalShopPurchasedComponentBulkImportProcessor, GlobalShopPurchasedComponentPlaceholder
from globalshop.importer.processors.raw_material import MaterialImportProcessor
from globalshop.integration.config_mixin import GlobalShopConfigMixin
from globalshop.part import Part, ItemHist, InventoryHist
from importer.processors.custom_table_record import CustomTableRecordImportProcessor
from importer.processors.vendor import VendorImportProcessor
from importer.processors.workcenter import WorkCenterImportProcessor
from baseintegration.integration import logger
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.utils.custom_table import ImportCustomTable

from globalshop.customer import Customer, Contact
from globalshop.importer.processors.account import AccountImportProcessor
from paperless.objects.components import PurchasedComponent
from globalshop.customtablerecord import CustomTableRecord
from globalshop.vendor import Vendor
from baseintegration.utils import get_last_action_datetime
from globalshop.workcenter import WorkCenter


class GlobalShopAccountImportListener:

    def __init__(self, integration):
        self.identifier = "import_account"
        self._integration = integration
        logger.info("GlobalShop account import listener was instantiated")

    def get_new(self, bulk=False) -> List[str]:
        """
        There is no last modified field on CUSTOMER_MASTER, so at this time
        all customers are selected.
        """
        logger.info("Checking for new accounts")
        database_minutes_offset = self._integration.config_yaml["Importers"].get("database_minutes_offset", 0)
        last_processed_datetime = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                           bulk=bulk, database_minutes_offset=database_minutes_offset)
        date_to_search = last_processed_datetime.strftime('%Y-%m-%d')
        time_to_search = last_processed_datetime.strftime('%H:%M:%S')
        customer_ids = self.get_customer_ids(date_to_search)
        contact_customer_ids = self.get_contact_customer_ids(date_to_search, time_to_search)
        customer_ids.extend(cust_id for cust_id in contact_customer_ids if cust_id not in customer_ids)
        logger.info(f"{len(customer_ids)} customer records found")
        return customer_ids

    def get_customer_ids(self, date_to_search: str):
        """ Separate this out as a helper function so it can be overridden if necessary. """
        where = f'(DATE_LAST_UPDATE >= \'{date_to_search}\')'

        return Customer.select_ids(where)

    def get_contact_customer_ids(self, date_to_search: str, time_to_search: str):
        where = f'(LAST_CHG_DATE > \'{date_to_search}\' OR ' \
                f'(LAST_CHG_TIME = \'{date_to_search}\' AND LAST_CHG_TIME > \'{time_to_search}\'))'

        return Contact.select_customer_ids(where)


class GlobalShopAccountImporter(GlobalShopConfigMixin, AccountImporter):

    def _register_listener(self):
        self.listener = GlobalShopAccountImportListener(self._integration)
        logger.info("Globalshop account listener was registered")

    def _register_default_processors(self):
        self.register_processor(Customer, AccountImportProcessor)

    def _process_account(self, account_id: str):
        logger.info(f"Account id is {str(account_id)}")

        with self.process_resource(Customer, account_id) as customer_rec:
            logger.debug(f"Customer Record: {customer_rec}")


class GlobalShopMaterialImportListener:

    def __init__(self, integration):
        self.identifier = "import_material"
        self._integration = integration
        logger.info("GlobalShop material import listener was instantiated")

    def get_new(self, bulk=False) -> List[str]:
        logger.info("Checking for new materials")
        new_material_ids = set()

        database_minutes_offset = self._integration.config_yaml["Importers"].get("database_minutes_offset", 0)
        last_processed_datetime = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                           bulk=bulk, database_minutes_offset=database_minutes_offset)
        date_to_search = last_processed_datetime.strftime('%Y-%m-%d')
        time_to_search = last_processed_datetime.strftime('%H:%M:%S')
        logger.info(f'Dates and time to search -> {date_to_search}, {time_to_search}')
        codes_to_include = self._integration.config_yaml["Importers"]["materials"].get("codes_to_include", [])
        codes_to_exclude = self._integration.config_yaml["Importers"]["materials"].get("codes_to_exclude", [])
        new_material_ids = self.get_part_ids(codes_to_exclude, codes_to_include, date_to_search, time_to_search)

        inventory_history_ids = self.get_inentory_part_ids(date_to_search, time_to_search)
        item_history_ids = self.get_item_history_part_ids(date_to_search, time_to_search)
        union_part_ids = set(new_material_ids) | set(inventory_history_ids) | set(item_history_ids)
        logger.info(f"Found {str(len(union_part_ids))} records to update")
        return union_part_ids

    @staticmethod
    def get_inentory_part_ids(date_to_search, time_to_search):
        where = f'(DATE_HISTORY > \'{date_to_search}\' OR ' \
                f'(DATE_HISTORY = \'{date_to_search}\' AND INV_HIST_TIME > \'{time_to_search}\')) AND '\
                "CODE_TRANSACTION IN ('R10', 'R11')"
        return InventoryHist.select_ids(where)

    @staticmethod
    def get_item_history_part_ids(date_to_search, time_to_search):
        where = f'(DATE_HISTORY > \'{date_to_search}\' OR ' \
                f'(DATE_HISTORY = \'{date_to_search}\' AND TIME_ITEM_HISTORY > \'{time_to_search}\')) AND '\
                "CODE_TRANSACTION IN ('R10', 'R11')"
        return ItemHist.select_ids(where)

    def get_part_ids(self, codes_to_exclude, codes_to_include, date_to_search, time_to_search):
        """ Separate this out as a helper function so it can be overridden if necessary. """
        where = f'(DATE_LAST_CHG > \'{date_to_search}\' OR ' \
                f'(DATE_LAST_CHG = \'{date_to_search}\' AND TIME_LAST_CHG > \'{time_to_search}\'))'
        if codes_to_include:
            include_in = ', '.join(f'\'{code}\'' for code in codes_to_include)
            where = f'{where} AND PRODUCT_LINE IN ({include_in})'
        if codes_to_exclude:
            exclude_in = ', '.join(f'\'{code}\'' for code in codes_to_exclude)
            where = f'{where} AND PRODUCT_LINE NOT IN ({exclude_in})'

        return Part.select_ids(where)


class GlobalShopMaterialImporter(GlobalShopConfigMixin, MaterialImporter):

    def _register_listener(self):
        self.listener = GlobalShopMaterialImportListener(self._integration)
        logger.info("GlobalShop material listener was registered")

    def _register_default_processors(self):
        self.register_processor(Part, MaterialImportProcessor)

    def check_custom_table_exists(self):
        logger.info("We're creating a header dictionary.")
        self.header_dict = {
            'material_id': 'Material ID',
            'mat_ext_desc': 'Material Ext Desc',
            'mat_desc': 'Description',
            'mat_qty_onhand': 'Qty On Hand',
            'mat_net_onhand': 'Net On Hand',
            'mat_rate': 'Rate',
            'mat_alt_rate': 'Mat Alt Rate',
            'mat_cost_date': 'Mat Cost Date',
            'mat_um_inventory': 'UM Inventory',
            'product_code': 'Product Line'
        }

        return ImportCustomTable.check_custom_header_custom_table_exists("gss_materials", self.header_dict,
                                                                         "material_id")

    def _process_material(self, material_id: str):
        logger.info(f"Material id is {str(material_id)}")

        with self.process_resource(Part, material_id) as part_rec:
            logger.debug(f"Part Record: {part_rec}")


class GlobalShopPurchasedComponentListener:

    def __init__(self, integration):
        self.identifier = "import_purchased_component"
        self._integration = integration
        logger.info("GlobalShop purchased component import listener was instantiated")

    def get_new(self, bulk=False):
        logger.info("Checking for new purchased components")
        database_minutes_offset = self._integration.config_yaml["Importers"].get("database_minutes_offset", 0)
        last_processed_datetime = get_last_action_datetime(self._integration.managed_integration_uuid,
                                                           self.identifier, bulk=bulk, database_minutes_offset=database_minutes_offset)
        date_to_search = last_processed_datetime.strftime('%Y-%m-%d')
        time_to_search = last_processed_datetime.strftime('%H:%M:%S')
        codes_to_include = self._integration.config_yaml["Importers"]["purchased_components"].get("codes_to_include",
                                                                                                  [])
        codes_to_exclude = self._integration.config_yaml["Importers"]["purchased_components"].get("codes_to_exclude",
                                                                                                  [])
        new_purchased_component_ids = self.get_part_ids(codes_to_exclude, codes_to_include, date_to_search,
                                                        time_to_search)
        inventory_history_ids = GlobalShopMaterialImportListener.get_inentory_part_ids(date_to_search, time_to_search)
        item_history_ids = GlobalShopMaterialImportListener.get_item_history_part_ids(date_to_search, time_to_search)
        union_part_ids = set(new_purchased_component_ids) | set(inventory_history_ids) | set(item_history_ids)

        logger.info(f"Found {str(len(union_part_ids))} records to update")
        return union_part_ids

    def get_part_ids(self, codes_to_exclude, codes_to_include, date_to_search, time_to_search):
        """ Separate this out as a helper function so it can be overridden if necessary. """
        where = f'(DATE_LAST_CHG > \'{date_to_search}\' OR '\
                f'(DATE_LAST_CHG = \'{date_to_search}\' AND TIME_LAST_CHG > \'{time_to_search}\'))'
        if codes_to_include:
            include_in = ', '.join(f'\'{code}\'' for code in codes_to_include)
            where = f'{where} AND PRODUCT_LINE IN ({include_in})'
        if codes_to_exclude:
            exclude_in = ', '.join(f'\'{code}\'' for code in codes_to_exclude)
            where = f'{where} AND PRODUCT_LINE NOT IN ({exclude_in})'

        return Part.select_ids(where)


class GlobalShopPurchasedComponentImporter(GlobalShopConfigMixin, PurchasedComponentImporter):

    def _register_listener(self):
        self.listener = GlobalShopPurchasedComponentListener(self._integration)
        logger.info("GlobalShop purchased component listener was registered")

    def _register_default_processors(self):
        self.register_processor(PurchasedComponent, GlobalShopPurchasedComponentImportProcessor)
        self.register_processor(GlobalShopPurchasedComponentPlaceholder, GlobalShopPurchasedComponentBulkImportProcessor)

    def _process_purchased_component(self, purchased_component_id: str):  # noqa: C901
        with self.process_resource(PurchasedComponent, purchased_component_id) as result:
            logger.info(f"Processed purchased component {str(purchased_component_id)}")
            return result

    def _bulk_process_purchased_component(self, purchased_component_ids: List[str]):
        with self.process_resource(GlobalShopPurchasedComponentPlaceholder, purchased_component_ids) as result:
            logger.info(f'Processed {len(purchased_component_ids)} purchased components')
            return result


class GlobalShopWorkCenterImportListener:

    def __init__(self, integration):
        self.identifier = "import_work_center"
        self._integration = integration
        logger.info("GlobalShop workcenter import listener was instantiated")

    def get_new(self, bulk=False) -> List[str]:
        logger.info("Checking for new workcenters")
        workcenter_ids = WorkCenter.select_ids()
        logger.info(f"{len(workcenter_ids)} workcenter records found")
        return workcenter_ids


class GlobalShopWorkCenterImporter(GlobalShopConfigMixin, WorkCenterImporter):

    def _register_listener(self):
        self.listener = GlobalShopWorkCenterImportListener(self._integration)
        logger.info("GlobalShop workcenter listener was registered")

    def _register_default_processors(self):
        self.register_processor(WorkCenter, WorkCenterImportProcessor)

    def check_custom_table_exists(self):
        logger.info("We're creating a header dictionary.")
        self.header_dict = {
            'workcenter': 'Workcenter',
            'wc_dept': 'Department',
            'standard_bill': 'Standard Bill',
            'standard_cost': 'Standard Cost',
            'standard_overhead': 'Standard Overhead',
            'fixed_ovhd': 'Fixed Ovhd',
            'wc_name': 'Name',
            'workgroup': 'Workgroup',
            'workgroup_descr': 'Workgroup Descr',
            'prototype_wc': 'Prototype WC'
        }

        return ImportCustomTable.check_custom_header_custom_table_exists("gss_workcenters", self.header_dict,
                                                                         "workcenter")

    def _process_work_center(self, work_center_id: str) -> bool:
        logger.info(f"WorkCenter id is {str(work_center_id)}")

        with self.process_resource(WorkCenter, work_center_id) as wc_rec:
            logger.debug(f"WorkCenter Record: {wc_rec}")
            return True


class GlobalShopVendorImportListener:

    def __init__(self, integration):
        self.identifier = "import_vendor"
        self._integration = integration
        logger.info("GlobalShop vendor import listener was instantiated")

    def get_new(self, bulk=False) -> List[str]:
        logger.info("Checking for new vendors")
        database_minutes_offset = self._integration.config_yaml["Importers"].get("database_minutes_offset", 0)
        last_processed_datetime = get_last_action_datetime(self._integration.managed_integration_uuid,
                                                           self.identifier, bulk=bulk, database_minutes_offset=database_minutes_offset)
        date_to_search = last_processed_datetime.strftime('%Y-%m-%d')
        time_to_search = last_processed_datetime.strftime('%H:%M:%S')
        vendor_ids = self.get_vendor_ids(date_to_search, time_to_search)
        logger.info(f"{len(vendor_ids)} vendor records found")
        return vendor_ids

    def get_vendor_ids(self, date_to_search, time_to_search):
        """ Separate this out as a helper function so it can be overridden if necessary. """
        where = f'(DATE_LAST_CHANGED > \'{date_to_search}\' OR '\
                f'(DATE_LAST_CHANGED = \'{date_to_search}\' AND TIME_LAST_CHANGED > \'{time_to_search}\'))'
        return Vendor.select_ids(where)


class GlobalShopVendorImporter(GlobalShopConfigMixin, VendorImporter):

    def _register_listener(self):
        self.listener = GlobalShopVendorImportListener(self._integration)
        logger.info("GlobalShop vendor listener was registered")

    def _register_default_processors(self):
        self.register_processor(Vendor, VendorImportProcessor)

    def check_custom_table_exists(self):
        logger.info("We're creating a header dictionary.")
        self.header_dict = {
            'vendor': 'Vendor',
            'name_vendor': 'Vendor Name'
        }

        return ImportCustomTable.check_custom_header_custom_table_exists("gss_vendors", self.header_dict,
                                                                         "vendor")

    def _process_vendor(self, vendor_id: str) -> bool:
        logger.info(f"Vendor id is {str(vendor_id)}")

        with self.process_resource(Vendor, vendor_id) as vendor_rec:
            logger.debug(f"Vendor Record: {vendor_rec}")
            return True


class GlobalShopCustomTableRecordImportListener:

    def __init__(self, integration):
        self.identifier = "import_custom_table_record"
        self._integration = integration
        logger.info("GlobalShop custom table record import listener was instantiated")

    def get_new(self, bulk=False) -> List[str]:
        logger.info("Checking for new records")
        database_minutes_offset = self._integration.config_yaml["Importers"].get("database_minutes_offset", 0)
        last_processed_datetime = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                           bulk=bulk, database_minutes_offset=database_minutes_offset)
        date_to_search = last_processed_datetime.strftime('%Y-%m-%d')
        time_to_search = last_processed_datetime.strftime('%H:%M:%S')
        codes_to_include = self._integration.config_yaml["Importers"]["custom_table"].get("codes_to_include", [])
        codes_to_exclude = self._integration.config_yaml["Importers"]["custom_table"].get("codes_to_exclude", [])
        new_record_ids = self.get_part_ids(codes_to_exclude, codes_to_include, date_to_search, time_to_search)

        logger.info(f"{len(new_record_ids)} records found")
        return new_record_ids

    def get_part_ids(self, codes_to_exclude, codes_to_include, date_to_search, time_to_search):
        """ Separate this out as a helper function so it can be overridden if necessary. """
        where = f'(DATE_LAST_CHG > \'{date_to_search}\' OR ' \
                f'(DATE_LAST_CHG = \'{date_to_search}\' AND TIME_LAST_CHG > \'{time_to_search}\')) ' \
                f'AND OBSOLETE_FLAG <> \'Y\''
        if codes_to_include:
            include_in = ', '.join(f'\'{code}\'' for code in codes_to_include)
            where = f'{where} AND PRODUCT_LINE IN ({include_in})'
        if codes_to_exclude:
            exclude_in = ', '.join(f'\'{code}\'' for code in codes_to_exclude)
            where = f'{where} AND PRODUCT_LINE NOT IN ({exclude_in})'

        return Part.select_ids(where)


class GlobalShopCustomTableRecordImporter(GlobalShopConfigMixin, CustomTableRecordImporter):

    def _register_listener(self):
        self.listener = GlobalShopCustomTableRecordImportListener(self._integration)
        logger.info("GlobalShop custom table record listener was registered")

    def _register_default_processors(self):
        self.register_processor(CustomTableRecord, CustomTableRecordImportProcessor)

    def _process_record(self, record_id: str) -> bool:
        logger.info(f"Record id is {str(record_id)}")

        with self.process_resource(CustomTableRecord, record_id) as powder_rec:
            logger.debug(f"Record: {powder_rec}")
            return True

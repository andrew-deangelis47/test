from typing import List
from baseintegration.datamigration import logger
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.importer.material_importer import MaterialImporter
from baseintegration.importer.outside_service_importer import OutsideServiceImporter
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from baseintegration.importer.vendor_importer import VendorImporter
from baseintegration.importer.work_center_importer import WorkCenterImporter

from baseintegration.utils import Vendor, OutsideService, Workcenter
from baseintegration.utils.custom_table import HexImportCustomTable

from paperless.objects.customers import Account
from paperless.objects.components import PurchasedComponent
from paperless.objects.components import Material

from mietrak_pro.importer.processors.account import AccountImportProcessor
from mietrak_pro.importer.processors.material import MaterialImportProcessor, BulkMaterialImportPlaceholder, \
    MieTrakProMaterialBulkImportProcessor
from mietrak_pro.importer.processors.outside_service import OutsideServiceImportProcessor
from mietrak_pro.importer.processors.purchased_component import MietrakProPurchasedComponentImportProcessor, \
    MietrakProPurchasedComponentPlaceholder, MietrakProPurchasedComponentBulkImportProcessor
from mietrak_pro.importer.configuration import CustomerImportConfig, MaterialImportConfig, OutsideServiceImportConfig, \
    PurchasedComponentImportConfig, WorkCenterImportConfig
from mietrak_pro.importer.processors.vendor import VendorImportProcessor
from mietrak_pro.importer.processors.workcenter import WorkCenterImportProcessor, BulkWorkCenterImportPlaceholder
from mietrak_pro.importer.utils import MietrakProImportListener
from baseintegration.utils.custom_table import CustomTable
from mietrak_pro.models.paperless_custom_tables import PurchaseOrderLineCustomTableFormat


class MietrakProAccountImportListener(MietrakProImportListener):

    def __init__(self, integration):
        super().__init__(integration, 'account_import', 'accounts', 'accounts')

    def _add_new_ids(self, ids: set, new_hex_counter: str, last_processed_decimal_counter: int,
                     minimum_primary_key_value) -> str:
        counter = get_hex(self, name='account_import')

        # Use a raw SQL query to get the Customer records newer than the last processed counter. The
        account_query = f"SELECT PartyPK, LastAccess FROM Party WHERE (LastAccess  >  " \
                        f"{counter} AND Customer=1 AND InactiveDate IS NULL)"
        new_hex_counter = self._add_ids_from_query(ids, new_hex_counter, account_query)

        # Use a raw SQL query to get the Contact records newer than the last processed counter.
        contact_query = "SELECT PartyBuyer.PartyFK, Party.LastAccess FROM Party " \
                        "INNER JOIN PartyBuyer ON Party.PartyPK=PartyBuyer.BuyerFK " \
                        f"WHERE (Party.LastAccess > {counter} " \
                        f"AND Party.Buyer = 1 AND InactiveDate IS NULL)"
        new_hex_counter = self._add_ids_from_query(ids, new_hex_counter, contact_query)

        # Use a raw SQL query to get the Address records newer than the last processed counter.
        address_query = "SELECT Address.PartyFK, Address.LastAccess FROM Address " \
                        "INNER JOIN Party ON Party.PartyPK=Address.PartyFK " \
                        f"WHERE (Address.LastAccess > {counter} " \
                        "AND Address.Archived = 0 AND Party.Customer=1 AND Party.InactiveDate IS NULL)"
        new_hex_counter = self._add_ids_from_query(ids, new_hex_counter, address_query)

        return new_hex_counter


class MietrakProAccountImporter(AccountImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            account_config = self._integration.config_yaml["Importers"]["accounts"]
            self.erp_config = CustomerImportConfig(
                should_import_sold_to_address=account_config.get("should_import_sold_to_address", True),
                should_import_billing_address=account_config.get("should_import_billing_address", True),
                should_import_shipping_addresses=account_config.get("should_import_shipping_addresses", True),
                should_import_contacts=account_config.get("should_import_contacts", True),
                should_skip_incomplete_addresses=account_config.get("should_skip_incomplete_addresses", True),
                should_skip_material_no_description=account_config.get("should_skip_material_no_description", False),
                should_use_customer_terms=account_config.get("should_use_customer_terms", False))
        else:
            self.erp_config = CustomerImportConfig(should_import_sold_to_address=True,
                                                   should_import_billing_address=True,
                                                   should_import_shipping_addresses=True,
                                                   should_import_contacts=True,
                                                   should_skip_incomplete_addresses=False,
                                                   should_use_customer_terms=False)

    def _register_listener(self):
        self.listener = MietrakProAccountImportListener(self._integration)
        logger.info("MIE Trak Pro account listener was registered")

    def _register_default_processors(self):
        self.register_processor(Account, AccountImportProcessor)

    def _process_account(self, account_id: str):  # noqa: C901
        logger.info(f"Processing account with id {account_id}")
        with self.process_resource(Account, account_id):
            logger.info(f"Processed account {str(account_id)}")


class MietrakProPurchasedComponentListener(MietrakProImportListener):

    def __init__(self, integration, erp_config: PurchasedComponentImportConfig):
        super().__init__(integration, 'purchased_component_import', 'purchased_components',
                         'purchased components')
        self.erp_config = erp_config

    def _get_new_query(self, last_processed_decimal_counter, minimum_primary_key_value):
        added_conditions = ""
        if self.erp_config.should_skip_inactive:
            added_conditions += " AND Item.InactiveDate IS NULL"

        counter = get_hex(self, name='purchased_component_import')

        return "SELECT Item.ItemPK, Item.LastAccess FROM Item " \
               "INNER JOIN ItemType ON Item.ItemTypeFK = ItemType.ItemTypePK " \
               "WHERE ItemType.Description = 'Hardware/Supplies' " \
               f"AND Item.LastAccess > {counter} " \
               f"AND Item.ItemPK >= {minimum_primary_key_value}{added_conditions} " \
               "UNION SELECT ItemInventoryPK, Iteminventory.LastAccess FROM Iteminventory " \
               "INNER JOIN Item ON ItemInventory.ItemInventoryPK = Item.ItemPK " \
               "INNER JOIN ItemType ON Item.ItemTypeFK = ItemType.ItemTypePK " \
               "WHERE ItemType.Description = 'Hardware/Supplies' AND " \
               f"Iteminventory.LastAccess > {counter}"


class MietrakProPurchasedComponentImporter(PurchasedComponentImporter):
    _paperless_purchase_order_line_table_model = PurchaseOrderLineCustomTableFormat()

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            purchased_components_config = self._integration.config_yaml["Importers"]["purchased_components"]
            self.erp_config = PurchasedComponentImportConfig(
                should_skip_inactive=purchased_components_config.get("should_skip_inactive", False),
                should_skip_non_inventory_items=purchased_components_config.get(
                    "should_skip_non_inventory_items", False
                ),
                should_import_category=purchased_components_config.get("should_import_category", False),
                should_import_leadtime=purchased_components_config.get("should_import_leadtime", False),
                should_import_po_history=purchased_components_config.get("should_import_po_history", False)
            )
        else:
            self.erp_config = PurchasedComponentImportConfig(should_skip_inactive=False,
                                                             should_skip_non_inventory_items=False,
                                                             should_import_category=False,
                                                             should_import_leadtime=False,
                                                             should_import_po_history=False)

    def _register_listener(self):
        self.listener = MietrakProPurchasedComponentListener(self._integration, self.erp_config)
        logger.info("MIE Trak Pro purchased component listener was registered")

    def _register_default_processors(self):
        self.register_processor(PurchasedComponent, MietrakProPurchasedComponentImportProcessor)
        self.register_processor(
            MietrakProPurchasedComponentPlaceholder,
            MietrakProPurchasedComponentBulkImportProcessor
        )

    def _process_purchased_component(self, purchased_component_id: str):  # noqa: C901
        with self.process_resource(PurchasedComponent, purchased_component_id) as success:
            logger.info(f"Processed purchased component {str(purchased_component_id)}")
            return success

    def _bulk_process_purchased_component(self, purchased_component_ids: List[str]):
        with self.process_resource(MietrakProPurchasedComponentPlaceholder, purchased_component_ids) as success:
            return success


class MietrakProMaterialImportListener(MietrakProImportListener):

    def __init__(self, integration, erp_config: MaterialImportConfig):
        super().__init__(integration, 'material_import', 'materials', 'materials')
        self.erp_config = erp_config

    def _get_new_query(self, last_processed_decimal_counter, minimum_primary_key_value):
        added_conditions = ""
        if self.erp_config.should_skip_inactive:
            added_conditions += " AND Item.InactiveDate IS NULL"
        if self.erp_config.should_skip_material_no_description:
            added_conditions += " AND Item.Description IS NOT NULL"
        logger.info(f'last_processed_decimal_counter - {last_processed_decimal_counter}')

        counter = get_hex(self, name='material_import')

        return "SELECT Item.ItemPK, Item.LastAccess FROM Item " \
               "INNER JOIN ItemType ON Item.ItemTypeFK = ItemType.ItemTypePK " \
               "WHERE ItemType.Description = 'Material' " \
               f"AND Item.LastAccess > {counter} AND Item.ItemPK >= " \
               f"{minimum_primary_key_value}{added_conditions} "  \
               "UNION SELECT ItemInventoryPK, Iteminventory.LastAccess FROM Iteminventory " \
               "INNER JOIN Item ON ItemInventory.ItemInventoryPK = Item.ItemPK " \
               "INNER JOIN ItemType ON Item.ItemTypeFK = ItemType.ItemTypePK " \
               "WHERE ItemType.Description = 'Material' AND " \
               f"Iteminventory.LastAccess > {counter}"


class MietrakProMaterialImporter(MaterialImporter):
    _paperless_purchase_order_line_table_model = PurchaseOrderLineCustomTableFormat()

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "materials"
            materials_config = self._integration.config_yaml["Importers"]["materials"]
            self.erp_config = MaterialImportConfig(
                should_skip_material_no_description=materials_config.get("should_skip_material_no_description", False),
                should_skip_inactive=materials_config.get("should_skip_inactive", False),
                should_import_category=materials_config.get("should_import_category", False),
                should_import_leadtime=materials_config.get("should_import_leadtime", False),
                should_import_vendor=materials_config.get("should_import_vendor", False),
                should_import_po_history=materials_config.get("should_import_po_history", False),
            )
        else:
            self.table_name = "mietrak_pro_materials"
            self.erp_config = MaterialImportConfig(should_skip_incomplete_addresses=False,
                                                   should_skip_inactive=False,
                                                   should_import_category=True,
                                                   should_import_leadtime=True,
                                                   should_import_vendor=True,
                                                   should_import_po_history=True)

    def _register_listener(self):
        self.listener = MietrakProMaterialImportListener(self._integration, self.erp_config)
        logger.info("MIE Trak Pro material listener was registered")

    def check_custom_table_exists(self):
        # TODO - add more fields
        self.header_dict = {
            "ItemPK": 1,
            "PartNumber": "",
            "Description": "",
            "LastCost": 0,
            "StockLength": 0,
            "StockWidth": 0,
            "Thickness": 0,
            "Weight": 0,
            "WeightFactor": 0,
            "SquareFootPerPound": 0
        }
        if self.erp_config.should_import_category is True:
            self.header_dict.update({"Category": ""})

        if self.erp_config.should_import_leadtime:
            self.header_dict.update({"Leadtime": 0})

        if self.erp_config.should_import_vendor:
            self.header_dict.update({"Vendor": ""})

        HexImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict,
                                                                     'ItemPK')
        if self.erp_config.should_import_po_history:
            self._paperless_purchase_order_line_table_model.check_custom_header_custom_table_exists()

    def _register_default_processors(self):
        self.register_processor(Material, MaterialImportProcessor)
        self.register_processor(BulkMaterialImportPlaceholder, MieTrakProMaterialBulkImportProcessor)

    def _process_material(self, material_id: str):  # noqa: C901
        with self.process_resource(Material, material_id):
            logger.info(f"Processed material {str(material_id)}")

    def _bulk_process_material(self, material_ids: List[str]):
        with self.process_resource(BulkMaterialImportPlaceholder, material_ids):
            logger.info(f"bulk processed {len(material_ids)} materials")


class MietrakProOutsideServiceImportListener(MietrakProImportListener):

    def __init__(self, integration, erp_config: OutsideServiceImportConfig):
        super().__init__(integration, 'outside_service_import', 'outside_services',
                         'outside services')
        self.erp_config = erp_config

    def _get_new_query(self, last_processed_decimal_counter, minimum_primary_key_value):
        added_conditions = ""
        if self.erp_config.part_number_exclusion_term:
            added_conditions += f" AND PartNumber NOT LIKE '%{self.erp_config.part_number_exclusion_term}%'"
        if self.erp_config.starting_year:
            added_conditions += f" AND Item.CreateDate > '{self.erp_config.starting_year}'"
        counter = get_hex(self, name='outside_service_import')
        return "SELECT Item.ItemPK, Item.LastAccess FROM Item " \
               "INNER JOIN ItemType ON Item.ItemTypeFK = ItemType.ItemTypePK " \
               "WHERE ItemType.Description = 'Outside Process' " \
               f"AND Item.LastAccess > {counter} AND Item.ItemPK >= {minimum_primary_key_value}{added_conditions}"


class MietrakProOutsideServiceImporter(OutsideServiceImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "outside_processes"
            outside_services_config = self._integration.config_yaml["Importers"]["outside_services"]
            self.erp_config = OutsideServiceImportConfig(
                part_number_exclusion_term=outside_services_config.get("part_number_exclusion_term"),
                starting_year=outside_services_config.get("starting_year"),
                should_import_category=outside_services_config.get("should_import_category", False),
                should_import_leadtime=outside_services_config.get("should_import_leadtime", False),
                should_import_costs=outside_services_config.get("should_import_costs", False)
            )
        else:
            self.table_name = "mietrak_pro_outside_processes"
            self.erp_config = OutsideServiceImportConfig(
                part_number_exclusion_term=None,
                starting_year=None,
                should_import_costs=True,
                should_import_category=True,
                should_import_leadtime=True
            )

    def _register_listener(self):
        self.listener = MietrakProOutsideServiceImportListener(self._integration, self.erp_config)
        logger.info("MIE Trak Pro outside service listener was registered")

    def check_custom_table_exists(self):
        self.header_dict = {
            "ItemPK": 1,
            "PartNumber": "",
            "VendorPartNumber": "",
            "Description": "",
            "Vendor": "",
            "PartyPK": 0
        }
        if self.erp_config.should_import_category is True:
            self.header_dict.update({"Category": ""})
        if self.erp_config.should_import_leadtime:
            self.header_dict.update({"Leadtime": 0})
        if self.erp_config.should_import_costs:
            for i in range(1, 11):
                self.header_dict.update({f'price{i}': 0})
                self.header_dict.update({f'quantity{i}': 0})
                self.header_dict.update({f'sellprice{i}': 0})

        HexImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict,
                                                                     'ItemPK')

    def _register_default_processors(self):
        self.register_processor(OutsideService, OutsideServiceImportProcessor)

    def _process_outside_service(self, service_id: str):
        with self.process_resource(OutsideService, service_id):
            logger.info(f"Processed outside service {str(service_id)}")


class MietrakProVendorImportListener(MietrakProImportListener):

    def __init__(self, integration):
        super().__init__(integration, 'vendor_import', 'vendors', 'vendors')

    def _get_new_query(self, last_processed_decimal_counter, minimum_primary_key_value):
        counter = get_hex(self, name='vendor_import')
        return f"SELECT PartyPK, LastAccess FROM Party WHERE " \
               f"(LastAccess > {counter} " \
               "AND Supplier = 1 AND InactiveDate IS NULL)"


class MietrakProVendorImporter(VendorImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "vendors"
        else:
            self.table_name = "mietrak_pro_vendors"

    def _register_listener(self):
        self.listener = MietrakProVendorImportListener(self._integration)
        logger.info("MIE Trak Pro vendor listener was registered")

    def check_custom_table_exists(self):
        self.header_dict = {
            "PartyPK": 1,
            "Name": "",
            "ShortName": "",
            "Phone": "",
            "Fax": "",
            "Email": "",
            "ShipVia": "",
            "ShipViaPK": 0
        }
        HexImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict,
                                                                     'PartyPK')

    def _register_default_processors(self):
        self.register_processor(Vendor, VendorImportProcessor)

    def _process_vendor(self, vendor_id: str):
        with self.process_resource(Vendor, vendor_id):
            logger.info(f"Processed vendor {str(vendor_id)}")


class MietrakProWorkCenterImportListener(MietrakProImportListener):

    def __init__(self, integration, erp_config: WorkCenterImportConfig):
        super().__init__(integration, 'work_center_import', 'work_centers',
                         'work_centers')
        self.erp_config = erp_config

    def _get_new_query(self, last_processed_decimal_counter, minimum_primary_key_value):
        return "SELECT OperationPK, LastAccess FROM Operation"


class MietrakProWorkCenterImporter(WorkCenterImporter):
    def _setup_erp_config(self):
        if not self._integration.test_mode:
            work_center_config = self._integration.config_yaml["Importers"]["work_centers"]
            self.table_name = "work_centers"
            self.erp_config = WorkCenterImportConfig(
                should_import_division=work_center_config.get("should_import_division")
            )
        else:
            self.table_name = "mietrak_pro_workcenters"
            self.erp_config = WorkCenterImportConfig(
                should_import_division=False
            )

    def _register_listener(self):
        self.listener = MietrakProWorkCenterImportListener(self._integration, self.erp_config)
        logger.info("MIE Trak Pro work center listener was registered")

    def check_custom_table_exists(self):
        self.header_dict = {
            "OperationPK": 1,
            "WorkCenterFK": 0,
            "WorkCenterDesc": "",
            "Name": "",
            "Description": "",
            "SetupOperationSellRate": 0,
            "SetupOperationProfitRate": 0,
            "SetupOperationOverHeadRate": 0,
            "SetupEmployeeRate": 0,
            "RunOperationSellRate": 0,
            "RunOperationProfitRate": 0,
            "RunOperationOverHeadRate": 0,
            "RunEmployeeRate": 0
        }

        if self.erp_config.should_import_division is True:
            self.header_dict.update({"DivisionFK": ""})

        HexImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict,
                                                                     'OperationPK')

    def _register_default_processors(self):
        self.register_processor(Workcenter, WorkCenterImportProcessor)

    def _process_work_center(self, work_center_id: str):
        with self.process_resource(Workcenter, work_center_id):
            logger.info(f"Processed work center {str(work_center_id)}")

    def _bulk_process_work_center(self, work_center_ids: List[str]):
        with self.process_resource(BulkWorkCenterImportPlaceholder, work_center_ids):
            logger.info(f"bulk processed {len(work_center_ids)} work centers")


def get_hex(cls, name: str):
    counter = 0
    for row in CustomTable.get('integration_state_info')['rows']:
        if 'process_type' in row:
            if row['process_type'] == name:
                counter = row['last_processed_hex_counter']
    return counter

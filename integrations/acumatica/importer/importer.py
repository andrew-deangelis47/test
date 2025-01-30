from dataclasses import dataclass
from typing import List

from paperless.objects.purchased_components import PurchasedComponent
from paperless.objects.components import Material

from baseintegration.datamigration import logger
from baseintegration.importer.work_center_importer import WorkCenterImporter
from baseintegration.utils import Vendor as PaperlessVendor, Workcenter, get_last_action_datetime, OutsideService as PaperlessOutsideService
from baseintegration.importer import BaseImporter
from baseintegration.importer.material_importer import MaterialImporter
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.importer.vendor_importer import VendorImporter
from baseintegration.importer.outside_service_importer import OutsideServiceImporter

from acumatica.api_models.paperless_custom_tables import WorkCenterCustomTableFormat, MaterialCustomTableFormat, \
    VendorCustomTableFormat, OutsideServiceCustomTableFormat

from acumatica.api_models.acumatica_models import Customer, StockItem, WorkCenter, Vendor, NonStockItem
from acumatica.importer.processors.workcenter import AcumaticaWorkCenterImportProcessor
from acumatica.importer.processors.materials import AcumaticaRawMaterialImportProcessor
from acumatica.importer.processors.purchased_component import AcumaticaPurchasedComponentImportProcessor
from acumatica.importer.processors.vendor import AcumaticaVendorImportProcessor
from acumatica.importer.processors.account import AccountImportProcessor
from acumatica.importer.processors.outside_service import AcumaticaOutsideServiceImportProcessor
from acumatica.importer.configuration import AcumaticaWorkCenterConfig, AcumaticaRawMaterialConfig, \
    AcumaticaPurchasedComponentConfig, AcumaticaVendorConfig, AcumaticaAccountConfig, AcumaticaOutsideServiceConfig
from acumatica.client import AcumaticaClient


RAW_MATERIAL_ITEM_CLASS = 'RAWMTL'
PC_ITEM_CLASS = 'PURCHASED'


@dataclass
class AcumaticaImporter(BaseImporter):
    def __init__(self, integration):
        super().__init__(integration)

    def _setup_erp_client(self):
        if not self._integration.test_mode:
            base_url = self._integration.secrets["Acumatica"]["base_url"]
            tenant = self._integration.secrets["Acumatica"]["tenant"]
            username = self._integration.secrets["Acumatica"]["username"]
            password = self._integration.secrets["Acumatica"]["password"]
            default_endpoint = self._integration.secrets["Acumatica"]["default_endpoint"]
            client_id = self._integration.secrets["Acumatica"]["client_id"]
            client_secret = self._integration.secrets["Acumatica"]["client_secret"]
            mfg_endpoint = self._integration.secrets["Acumatica"]["mfg_endpoint"]
            bearer_token = self._integration.secrets["Acumatica"]["bearer_token"]
            # Todo: This doesn't actually test if client is valid, its going to be a silent failure
            self.client = AcumaticaClient(base_url=base_url, username=username, password=password, tenant=tenant,
                                          default_endpoint=default_endpoint, mfg_endpoint=mfg_endpoint,
                                          bearer_token=bearer_token, client_id=client_id, client_secret=client_secret)
        else:
            self.client = AcumaticaClient(api_key="test", base_url="http://testapi.com", username="test", password="test")
        self._integration.api_client = self.client

    def check_custom_table_exists(self):
        self.add_or_remove_custom_table_attributes()
        self._paperless_table_model.check_custom_header_custom_table_exists()

    def add_or_remove_custom_table_attributes(self):
        """
        - Override this class and use the setattr() or delattr() functions to add or remove attributes to or from the
        custom table format.
        - Examples:
            - setattr(self._paperless_table_model, "new_atrribute", "xyz123")
            - delattr(self._paperless_table_model, "part_num")
        NOTE: You will also need to override the set_table_row_attributes() function in the "materials" import processor
        to correspond with your updated class attributes
        """
        pass


@dataclass
class AcumaticaWorkCenterImportListener:

    def __init__(self, integration):
        self.identifier = "import_work_center"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Returns ids (and object types) in a list of ALL operations, resource groups, and resources.
        - These entities do not have a last date modified field.
        """
        # Get config parameters that will be used as inputs for the query
        self.erp_config = AcumaticaWorkCenterConfig(self._integration.config_yaml)

        # Get the list of workcenters to process

        workcenters = WorkCenter.get_all()
        workcenter_list = list()
        for workcenter in workcenters:
            wc_id = workcenter.id
            workcenter_list.append(wc_id)
        return workcenter_list


class AcumaticaWorkCenterImporter(WorkCenterImporter, AcumaticaImporter):
    _paperless_operation_table_model = WorkCenterCustomTableFormat()

    def _register_listener(self):
        self.listener = AcumaticaWorkCenterImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Workcenter, AcumaticaWorkCenterImportProcessor)
        logger.info('Registered work center processor.')

    def _process_work_center(self, work_center_id: str):  # noqa: C901
        logger.info(f"Work center is {work_center_id}")
        with self.process_resource(Workcenter, work_center_id):
            logger.info(f"Processed work center id: {work_center_id}")

    def check_custom_table_exists(self):
        self.add_or_remove_custom_table_attributes()
        self._paperless_operation_table_model.check_custom_header_custom_table_exists()


@dataclass
class AcumaticaAccountImportListener:
    identifier: str = "import_account"

    def __init__(self, integration):
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        self.erp_config = AcumaticaAccountConfig(self._integration.config_yaml)
        date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                  bulk=bulk)

        # Get the list of materials to process
        last_mod_str = date_to_search.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        final_query = {
            '$filter': f"LastModifiedDateTime gt datetimeoffset'{last_mod_str}'",
            '$expand': 'Contacts,BillingContact/Address,ShippingContact/Address',
            '$top': '99999'
        }

        customers = Customer.get_changed(final_query)
        customer_list = list()
        for cust in customers:
            cust: Customer
            customer_list.append(cust.CustomerID)  # TODO id or CustID?
        return customer_list


class AcumaticaAccountImporter(AccountImporter, AcumaticaImporter):
    def _register_listener(self):
        self.listener = AcumaticaAccountImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Customer, AccountImportProcessor)
        logger.info('Registered account processor.')

    def _setup_erp_config(self):
        self.erp_config = AcumaticaAccountConfig(self._integration.config_yaml)

    def _process_account(self, account_id: str):
        logger.info(f"Account id is {str(account_id)}")
        with self.process_resource(Customer, account_id):
            logger.info(f"Processed account id: {account_id}")


@dataclass
class AcumaticaRawMaterialImportListener:
    identifier: str = "import_material"

    def __init__(self, integration):
        self.identifier = "import_material"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Listens for changes to part numbers of config-specified ClassIDs based on ChangedOn dates
        - Returns string type part numbers in a list.
        """
        self.erp_config = AcumaticaRawMaterialConfig(self._integration.config_yaml)
        date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                  bulk=bulk)

        # Get the list of materials to process

        last_mod_str = date_to_search.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        final_query = {
            '$filter': f"LastModified gt datetimeoffset'{last_mod_str}' and ItemClass eq '{self.erp_config.raw_material_item_class}'",
            '$top': '99999'
        }
        materials = StockItem.get_changed(final_query)
        material_list = list()
        for material in materials:
            material_id = material.InventoryID
            material_list.append(material_id)
        return material_list


class AcumaticaMaterialImporter(MaterialImporter, AcumaticaImporter):
    _paperless_table_model = MaterialCustomTableFormat()

    def _register_listener(self):
        self.listener = AcumaticaRawMaterialImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Material, AcumaticaRawMaterialImportProcessor)
        logger.info('Registered material processor')

    def _process_material(self, inventory_id: str):
        logger.info(f"Material inventory ID is {inventory_id}")
        with self.process_resource(Material, inventory_id):
            logger.info(f"Processed Material id: {inventory_id}")

    def _setup_erp_config(self):
        self.erp_config = AcumaticaRawMaterialConfig(self._integration.config_yaml)

    def check_custom_table_exists(self):
        logger.info('Checking if materials table exists')
        self.add_or_remove_custom_table_attributes()
        self._paperless_table_model.check_custom_header_custom_table_exists()


@dataclass
class AcumaticaPurchasedComponentImportListener:
    identifier: str = "import_purchased_component"

    def __init__(self, integration):
        self.identifier = "import_purchased_component"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Listens for changes to part numbers of config-specified ClassIDs based on ChangedOn dates
        - Returns string type part numbers in a list.
        """
        self.erp_config = AcumaticaPurchasedComponentConfig(self._integration.config_yaml)
        date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                  bulk=bulk)

        # interval_mins = self.erp_config.interval_mins
        # today = datetime.today()
        # yesterday = today - timedelta(days=interval_mins)

        # Get the list of materials to process

        last_mod_str = date_to_search.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        final_query = {
            '$filter': f"LastModified gt datetimeoffset'{last_mod_str}' and ItemClass eq '{self.erp_config.pc_item_class}'",
            '$top': '99999'
        }
        # Get the list of materials to process
        purchased_component_list = list()
        purchased_component_response = StockItem.get_changed(final_query)

        for purchased_component in purchased_component_response:
            purchased_component_list.append(purchased_component.InventoryID)
        return purchased_component_list


class AcumaticaPurchasedComponentImporter(PurchasedComponentImporter, AcumaticaImporter):
    def _register_listener(self):
        self.listener = AcumaticaPurchasedComponentImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(PurchasedComponent, AcumaticaPurchasedComponentImportProcessor)
        logger.info('Registered purchased component processor')

    def _process_purchased_component(self, component_id: str):
        logger.info(f"Purchased component id is {component_id}")
        with self.process_resource(PurchasedComponent, component_id):
            logger.info(f"Processed purchased component id: {component_id}")

    def _setup_erp_config(self):
        self.erp_config = AcumaticaPurchasedComponentConfig(self._integration.config_yaml)


@dataclass
class AcumaticaVendorImportListener:
    identifier: str = "import_vendors"

    def __init__(self, integration):
        self.identifier = "import_vendors"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Listens for changes to part numbers of config-specified ClassIDs based on ChangedOn dates
        - Returns string type part numbers in a list.
        """
        self.erp_config = AcumaticaVendorConfig(self._integration.config_yaml)
        date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                  bulk=bulk)

        last_mod_str = date_to_search.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        final_query = {
            '$filter': f"LastModifiedDateTime gt datetimeoffset'{last_mod_str}'",
            '$top': '99999'
        }

        # Get the list of materials to process
        vendor_response = Vendor.get_changed(final_query)
        vendor_list = list()
        logger.info(vendor_response)
        for vendor in vendor_response:
            vendor: Vendor
            vendor_list.append(vendor.VendorID)
        return vendor_list


class AcumaticaVendorImporter(VendorImporter, AcumaticaImporter):
    _paperless_operation_table_model = VendorCustomTableFormat()

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "vendors"
        else:
            self.table_name = "acumatica_vendors"

    def _register_listener(self):
        self.listener = AcumaticaVendorImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(PaperlessVendor, AcumaticaVendorImportProcessor)
        logger.info('Registered vendor processor.')

    def _process_vendor(self, vendor_id: str):  # noqa: C901
        logger.info(f"Vendor ID is {vendor_id}")
        with self.process_resource(PaperlessVendor, vendor_id):
            logger.info(f"Processed vendor id: {vendor_id}")

    def check_custom_table_exists(self):
        self.add_or_remove_custom_table_attributes()
        self._paperless_operation_table_model.check_custom_header_custom_table_exists()


@dataclass
class AcumaticaOutsideServiceImportListener:
    identifier: str = "outside_services"

    def __init__(self, integration):
        self.identifier = "outside_services"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Listens for changes to part numbers of config-specified ClassIDs based on ChangedOn dates
        - Returns string type part numbers in a list.
        """
        self.erp_config = AcumaticaOutsideServiceConfig(self._integration.config_yaml)
        date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier,
                                                  bulk=bulk)

        item_class = self.erp_config.outside_service_item_class
        last_mod_str = date_to_search.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        final_query = {
            '$filter': f"LastModifiedDateTime gt datetimeoffset'{last_mod_str}' and ItemClass eq '{item_class}'",
            "$expand": "VendorDetails",
            '$top': '99999'
        }

        # Get the list of materials to process
        non_stock_item_response = NonStockItem.get_changed(final_query)
        non_stock_list = list()
        logger.info(non_stock_item_response)
        for non_stock_item in non_stock_item_response:
            non_stock_item: NonStockItem
            non_stock_list.append(non_stock_item.InventoryID)

        return non_stock_list


class AcumaticaOutsideServiceImporter(OutsideServiceImporter, AcumaticaImporter):
    _paperless_operation_table_model = OutsideServiceCustomTableFormat()

    def _register_listener(self):
        self.listener = AcumaticaOutsideServiceImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(PaperlessOutsideService, AcumaticaOutsideServiceImportProcessor)
        logger.info('Registered outside service processor.')

    def _process_outside_service(self, service_id: str):  # noqa: C901
        logger.info(f"Service ID is {service_id}")
        with self.process_resource(PaperlessOutsideService, service_id):
            logger.info(f"Service vendor id: {service_id}")

    def check_custom_table_exists(self):
        self.add_or_remove_custom_table_attributes()
        self._paperless_operation_table_model.check_custom_header_custom_table_exists()

from dataclasses import dataclass
from typing import List, Optional
from epicor.importer.epicor_client_cache import EpicorClientCache
from baseintegration.datamigration import logger
from baseintegration.importer.work_center_importer import WorkCenterImporter
from baseintegration.utils import Vendor as PaperlessVendor, Workcenter, get_last_action_datetime
from paperless.objects.purchased_components import PurchasedComponent
from paperless.objects.components import Material
from epicor.client import EpicorClient
from baseintegration.importer import BaseImporter
from baseintegration.importer.material_importer import MaterialImporter
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.importer.vendor_importer import VendorImporter
from epicor.api_models.paperless_custom_tables import MaterialCustomTableFormat, VendorCustomTableFormat, \
    OperationCustomTableFormat, ResourceCustomTableFormat, ResourceGroupCustomTableFormat, OperationDetailsCustomTableFormat
from epicor.importer.processors.materials import EpicorRawMaterialImportProcessor, EpicorMaterialBulkPlaceholder, \
    EpicorBulkRawMaterialImportProcessor
from epicor.importer.processors.account import AccountImportProcessor
from epicor.importer.processors.purchased_component import EpicorPurchasedComponentImportProcessor, \
    EpicorPurchasedComponentBulkPlaceholder, EpicorPurchasedComponentBulkImportProcessor
from epicor.importer.configuration import EpicorRawMaterialConfig, EpicorPurchasedComponentConfig, \
    EpicorWorkCenterConfig
from epicor.customer import Customer, Contact
from epicor.importer.processors.work_center import EpicorWorkCenterImportProcessor, WorkCenterBulkPlaceholder, \
    EpicorWorkCenterBulkImportProcessor
from epicor.operation import Operation, ResourceGroup, Resource, OperationDetails
from epicor.part import PurchasedComponentPart as EpicorPurchasedComponentHelper
from epicor.part import MaterialPart as EpicorMaterialHelper
from epicor.utils import WorkCenterIDData
from epicor.vendor import Vendor
from epicor.importer.processors.vendor import EpicorVendorImportProcessor, VendorBulkPlaceholder, \
    EpicorVendorBulkImportProcessor


@dataclass
class EpicorImporter(BaseImporter):
    def __init__(self, integration):
        super().__init__(integration)
        self.epicor_client_cache: Optional[EpicorClientCache()] = None

    def _setup_erp_client(self):
        if not self._integration.test_mode:
            epicor_yaml = self._integration.config_yaml["Epicor"]
            api_url = self._integration.secrets["Epicor"]["base_url"]
            api_key = self._integration.secrets["Epicor"]["api_key"]
            username = self._integration.secrets["Epicor"]["username"]
            password = self._integration.secrets["Epicor"]["password"]
            bearer_token = self._integration.secrets["Epicor"].get("bearer_token", None)
            company_name = epicor_yaml.get("company_name", None)
            plant_code = epicor_yaml.get("plant_code", None)
            # Todo: This doesn't actually test if client is valid, its going to be a silent failure
            self.client = EpicorClient(api_key=api_key, base_url=api_url, username=username, password=password,
                                       bearer_token=bearer_token, company_name=company_name,
                                       plant_code=plant_code)
        else:
            self.client = EpicorClient(api_key="test", base_url="http://testapi.com", username="test", password="test")
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
class EpicorAccountImportListener:
    identifier: str = "import_account"

    def __init__(self, integration):
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        new_customers = set()
        date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)

        # get modified customers
        customers: List[Customer] = Customer.get_changed(date_to_search)
        customer_ids = [cust.CustID for cust in customers]
        new_customers.update(customer_ids)

        # get modified contacts
        contacts = Contact.get_changed(date_to_search)
        for contact in contacts:
            cust_id = contact.CustNumCustID
            if cust_id:
                new_customers.add(cust_id)

        return list(new_customers)


class EpicorAccountImporter(AccountImporter, EpicorImporter):
    def _register_listener(self):
        self.listener = EpicorAccountImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Customer, AccountImportProcessor)
        logger.info('Registered account processor.')

    def _process_account(self, account_id: str):
        logger.info(f"Account id is {str(account_id)}")
        with self.process_resource(Customer, account_id):
            logger.info(f"Processed account id: {account_id}")


@dataclass
class EpicorPurchasedComponentImportListener:
    _epicor_client: EpicorPurchasedComponentHelper = EpicorPurchasedComponentHelper
    identifier: str = "import_purchased_component"

    def __init__(self, integration):
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Listens for changes to part numbers of config-specified ClassIDs based on ChangedOn dates
        - Returns string type part numbers in a list.
        """
        # Get config parameters that will be used as inputs for the query
        self.erp_config = EpicorPurchasedComponentConfig(self._integration.config_yaml)
        date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        included_class_ids = self.erp_config.should_include_purchased_component_class_ids
        should_include_null_dates = True if self.erp_config.should_include_null_dates and bulk else False

        # Construct filter query based on config options
        material_query_filter = dict(TypeCode=["P"], ClassID=included_class_ids, ChangedOn=date_to_search)
        filter_query = self._epicor_client.construct_query_filter(material_query_filter, should_include_null_dates)
        final_query = {
            '$filter': filter_query,
            '$top': f'{self.erp_config.returned_record_limit}'
        }  # $top param allows API to return more than 100 results

        # Get list of parts to process
        parts_list = self._epicor_client.get_new_or_updated_parts_list(final_query)
        return parts_list


class EpicorPurchasedComponentImporter(PurchasedComponentImporter, EpicorImporter):

    def _register_listener(self):
        self.listener = EpicorPurchasedComponentImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(PurchasedComponent, EpicorPurchasedComponentImportProcessor)
        self.register_processor(EpicorPurchasedComponentBulkPlaceholder, EpicorPurchasedComponentBulkImportProcessor)
        logger.info('Registered purchased component processor.')

    def _process_purchased_component(self, component_id: str):  # noqa: C901
        logger.info(f"Purchased component id is {str(component_id)}")
        with self.process_resource(PurchasedComponent, component_id):
            logger.info(f"Processed purchased component id: {component_id}")

    def _bulk_process_purchased_component(self, purchased_component_ids: List[str]):
        with self.process_resource(EpicorPurchasedComponentBulkPlaceholder, purchased_component_ids) as success:
            logger.info(f"Bulk processed {len(purchased_component_ids)} purchased components")
            return success

    def _setup_erp_config(self):
        self.erp_config = EpicorPurchasedComponentConfig(self._integration.config_yaml)


@dataclass
class EpicorRawMaterialImportListener:
    _epicor_client: EpicorMaterialHelper = EpicorMaterialHelper
    identifier: str = "import_material"

    def __init__(self, integration):
        self.identifier = "import_material"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Listens for changes to part numbers of config-specified ClassIDs based on ChangedOn dates
        - Returns string type part numbers in a list.
        """
        # Get config parameters that will be used as inputs for the query
        self.erp_config = EpicorRawMaterialConfig(self._integration.config_yaml)
        date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        included_class_ids = self.erp_config.include_raw_material_class_ids
        should_include_null_dates = True if self.erp_config.should_include_null_dates and bulk else False

        # Construct filter query based on config options
        material_query_filter = dict(TypeCode=["P"], ClassID=included_class_ids, ChangedOn=date_to_search)
        filter_query = self._epicor_client.construct_query_filter(material_query_filter, should_include_null_dates)
        final_query = {
            '$filter': filter_query,
            '$top': f'{self.erp_config.returned_record_limit}'
        }  # $top param allows API to return more than 100 results

        # Get list of parts to process
        parts_list = self._epicor_client.get_new_or_updated_parts_list(final_query)
        return parts_list


class EpicorMaterialImporter(MaterialImporter, EpicorImporter):
    _paperless_table_model = MaterialCustomTableFormat()

    def _register_listener(self):
        self.listener = EpicorRawMaterialImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Material, EpicorRawMaterialImportProcessor)
        self.register_processor(EpicorMaterialBulkPlaceholder, EpicorBulkRawMaterialImportProcessor)
        logger.info('Registered material processor.')

    def _process_material(self, material_id: str):  # noqa: C901
        logger.info(f"Material id is {str(material_id)}")
        with self.process_resource(Material, material_id):
            logger.info(f"Processed Material id: {material_id}")

    def _bulk_process_material(self, material_ids: List[str]):  # noqa: C901
        with self.process_resource(EpicorMaterialBulkPlaceholder, material_ids) as success:
            logger.info(f"Bulk processed {len(material_ids)} materials")
            return success

    def _setup_erp_config(self):
        self.erp_config = EpicorRawMaterialConfig(self._integration.config_yaml)

    def check_custom_table_exists(self):
        self.add_or_remove_custom_table_attributes()
        self._paperless_table_model.check_custom_header_custom_table_exists()


@dataclass
class EpicorVendorImportListener:

    def __init__(self, integration):
        self.identifier = "import_vendor"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - No ChangedOn date exists for Epicor Vendors - all vendors are synced every time.
        """
        # get all vendors
        vendors: List[Vendor] = Vendor.get_paginated_results_with_params(params={}, page_size=50)

        # Convert to list of vendor IDs to process
        vendor_ids = [vend.VendorID for vend in vendors]
        return vendor_ids


class EpicorVendorImporter(VendorImporter, EpicorImporter):
    _paperless_table_model = VendorCustomTableFormat()

    def _register_listener(self):
        self.listener = EpicorVendorImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(PaperlessVendor, EpicorVendorImportProcessor)
        self.register_processor(VendorBulkPlaceholder, EpicorVendorBulkImportProcessor)
        logger.info('Registered vendor processor.')

    def _process_vendor(self, vendor_id: str):  # noqa: C901
        logger.info(f"Vendor id is {str(vendor_id)}")
        with self.process_resource(PaperlessVendor, vendor_id):
            logger.info(f"Processed vendor id: {vendor_id}")

    def _bulk_process_vendor(self, vendor_ids: List[str]):
        with self.process_resource(VendorBulkPlaceholder, vendor_ids) as success:
            logger.info(f"Bulk processed {len(vendor_ids)} vendors")
            return success

    def check_custom_table_exists(self):
        self.add_or_remove_custom_table_attributes()
        self._paperless_table_model.check_custom_header_custom_table_exists()


@dataclass
class EpicorWorkCenterImportListener:

    def __init__(self, integration):
        self.identifier = "import_work_center"
        self._integration = integration

    def get_new(self, bulk=False) -> List[str]:
        """
        - Returns ids (and object types) in a list of ALL operations, resource groups, and resources.
        - These entities do not have a last date modified field.
        """
        # Get config parameters that will be used as inputs for the query
        self.erp_config = EpicorWorkCenterConfig(self._integration.config_yaml)
        work_center_list = []

        # Specify any filters or parameters to be supplied to the get_all() function
        filters = {}
        params = {
            "$top": int(self.erp_config.returned_record_limit)
        }

        # get modified operations
        operations: List[Operation] = Operation.get_all(filters, params)
        operation_list = [
            self._get_work_center_type_string_representation(WorkCenterIDData(Operation, operation.OpCode))
            for operation in operations
        ]
        work_center_list.extend(operation_list)

        if self.erp_config.should_import_resource_groups:
            # get modified resource groups
            resource_groups: List[ResourceGroup] = ResourceGroup.get_all(filters, params)
            resource_group_list = [
                self._get_work_center_type_string_representation(
                    WorkCenterIDData(ResourceGroup, resource_group.ResourceGrpID)
                ) for resource_group in resource_groups
            ]
            work_center_list.extend(resource_group_list)

        if self.erp_config.should_import_resources:
            # get modified resources
            resources: List[Resource] = Resource.get_all(filters, params)
            resource_list = [
                self._get_work_center_type_string_representation(
                    WorkCenterIDData(Resource, resource.ResourceID)) for resource in resources
            ]
            work_center_list.extend(resource_list)

        if self.erp_config.should_map_multi_resource_group:
            # get modified resource group to operation mappings
            op_dtls: List[OperationDetails] = OperationDetails.get_all(filters, params)
            op_dtls_list = [
                self._get_work_center_type_string_representation(
                    WorkCenterIDData(OperationDetails,
                                     str(op_dtl.OpCode) + "~~" + str(op_dtl.ResourceGrpID))) for op_dtl in op_dtls
            ]
            work_center_list.extend(op_dtls_list)

        return work_center_list

    def _get_work_center_type_string_representation(self, work_center: WorkCenterIDData):
        if work_center.type == Operation:
            return f"{work_center.id}::operation"
        elif work_center.type == ResourceGroup:
            return f"{work_center.id}::resource_group"
        elif work_center.type == Resource:
            return f"{work_center.id}::resource"
        elif work_center.type == OperationDetails:
            return f"{work_center.id}::operation_details"
        else:
            logger.info("This is not a valid type of work center.")
            return None


class EpicorWorkCenterImporter(WorkCenterImporter, EpicorImporter):
    _paperless_operation_table_model = OperationCustomTableFormat()
    _paperless_resource_table_model = ResourceCustomTableFormat()
    _paperless_resource_group_table_model = ResourceGroupCustomTableFormat()
    _paperless_operation_details_table_model = OperationDetailsCustomTableFormat()

    def _register_listener(self):
        self.listener = EpicorWorkCenterImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Workcenter, EpicorWorkCenterImportProcessor)
        self.register_processor(WorkCenterBulkPlaceholder, EpicorWorkCenterBulkImportProcessor)
        logger.info('Registered work center processor.')

    def _process_work_center(self, work_center_id: str):  # noqa: C901
        logger.info(f"Work center is {work_center_id}")
        with self.process_resource(Workcenter, work_center_id):
            logger.info(f"Processed work center id: {work_center_id}")

    def _bulk_process_work_center(self, work_center_ids: List[str]):
        with self.process_resource(WorkCenterBulkPlaceholder, work_center_ids) as success:
            logger.info(f"Bulk processed {len(work_center_ids)} work centers")
            return success

    def check_custom_table_exists(self):
        self.add_or_remove_custom_table_attributes()
        self._paperless_operation_table_model.check_custom_header_custom_table_exists()
        self._paperless_resource_table_model.check_custom_header_custom_table_exists()
        self._paperless_resource_group_table_model.check_custom_header_custom_table_exists()
        self._paperless_operation_details_table_model.check_custom_header_custom_table_exists()

    def _setup_erp_config(self):
        self.erp_config = EpicorWorkCenterConfig(self._integration.config_yaml)

from types import SimpleNamespace
from typing import Type, List

from baseintegration.importer.work_center_importer import WorkCenterImporter

from baseintegration.datamigration import logger
from baseintegration.importer import BaseImporter
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.importer.material_importer import MaterialImporter
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from baseintegration.utils.custom_table import ImportCustomTable
from dynamics.exceptions import DynamicsNotFoundException
from dynamics.importer.processors.machine_centers import DynamicsMachineCenterImportProcessor, \
    MachineCenterBulkPlaceholder, DynamicsMachineCenterBulkImportProcessor
from dynamics.importer.processors.materials import DynamicsMaterialImportProcessor, DynamicsMaterialBulkPlaceholder, \
    DynamicsBulkMaterialImportProcessor

from paperless.objects.components import PurchasedComponent
from paperless.objects.customers import Account

from dynamics.client_factory import ClientFactory, ConfigFactory
from dynamics.importer.processors.accounts_contacts import AccountImportProcessor
from dynamics.importer.processors.purchased_component import DynamicsPurchasedComponentImportProcessor, \
    DynamicsPurchasedComponentBulkPlaceholder, DynamicsBulkPurchasedComponentImportProcessor
from dynamics.objects.base import BaseObject
from dynamics.objects.customer import Customer, Contact
from dynamics.objects.item import PurchasedComponent as DynamicsPurchasedComponent, Material, CoatingItem, RawMaterial, \
    MachineCenter
from baseintegration.utils import get_last_action_datetime
from baseintegration.integration import Integration


class DynamicsImportListener:
    def __init__(self, integration: Integration, identifier: str, object_type: Type[BaseObject]):
        self._integration = integration
        self.identifier = identifier
        self.object_type = object_type

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        updated_query_set = self.object_type.get_all_modified_after(date_to_search)
        return [obj.No for obj in updated_query_set]


class DynamicsImporter(BaseImporter):
    config_name: str

    def _setup_erp_config(self):
        if self._integration.test_mode:
            self.erp_config = SimpleNamespace()
        else:
            config_yaml = self._integration.config_yaml["Importers"][self.config_name]
            self.erp_config = ConfigFactory.build_config(config_yaml)

        self.dynamics_client = ClientFactory.build_client_from_config(
            self._integration.secrets, self._integration.test_mode
        )


class DynamicsAccountImportListener:
    def __init__(self, integration):
        self._integration = integration
        self.identifier = 'import_account'

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        # first get the updated customers
        updated_query_set = Customer.get_all_modified_after(date_to_search)
        updated_query_set = [cust.No for cust in updated_query_set]
        # next get the updated contacts
        updated_contacts = Contact.get_all_modified_after(date_to_search)
        for contact in updated_contacts:
            try:
                # find the customer that the contact is associated with
                customer = Customer.get_first({
                    "Name": contact.Company_Name
                })
            except DynamicsNotFoundException:
                # contact not linked to a customer, skip import
                pass
            else:
                if customer.No not in updated_query_set:
                    updated_query_set.append(customer.No)

        return updated_query_set


class DynamicsAccountImporter(AccountImporter, DynamicsImporter):
    config_name = 'accounts'

    def _register_listener(self):
        self.listener = DynamicsAccountImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Account, AccountImportProcessor)
        logger.info('Registered account processor.')

    def _process_account(self, account_id: str):
        logger.info(f"Processing Dynamics customer id: {account_id}")
        with self.process_resource(Account, account_id):
            logger.info(f"Processed Dynamics customer id is {account_id}")


class DynamicsPurchasedComponentImporter(PurchasedComponentImporter, DynamicsImporter):
    config_name = 'purchased_components'

    def _register_listener(self):
        self.listener = DynamicsImportListener(self._integration, 'import_purchased_component',
                                               DynamicsPurchasedComponent)

    def _register_default_processors(self):
        self.register_processor(PurchasedComponent, DynamicsPurchasedComponentImportProcessor)
        self.register_processor(DynamicsPurchasedComponentBulkPlaceholder, DynamicsBulkPurchasedComponentImportProcessor)
        logger.info('Registered purchased component processor.')

    def _process_purchased_component(self, purchased_component_id: str):
        logger.info(f"Purchased component id is {str(purchased_component_id)}")
        with self.process_resource(PurchasedComponent, purchased_component_id):
            logger.info(f"Processed purchased component id: {purchased_component_id}")

    def _bulk_process_purchased_component(self, purchased_component_ids: List[str]):
        with self.process_resource(DynamicsPurchasedComponentBulkPlaceholder, purchased_component_ids) as success:
            logger.info(f"Bulk processed {len(purchased_component_ids)} purchased components")
            return success


class DynamicsMaterialImportListener:
    def __init__(self, integration):
        self._integration = integration
        self.identifier = 'import_material'

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        updated_materials_query_set = Material.get_all_modified_after(date_to_search)
        updated_coating_items_query_set = CoatingItem.get_all_modified_after(date_to_search)
        updated_raw_materials = [*updated_materials_query_set, *updated_coating_items_query_set]
        updated_query_set = [item.No for item in updated_raw_materials]
        return updated_query_set


class DynamicsMaterialImporter(MaterialImporter, DynamicsImporter):
    config_name = 'materials'
    materials_table_name = 'dynamics-materials'
    coating_items_table_name = 'dynamics-coating-items'

    def _register_listener(self):
        self.listener = DynamicsMaterialImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(RawMaterial, DynamicsMaterialImportProcessor)
        self.register_processor(DynamicsMaterialBulkPlaceholder, DynamicsBulkMaterialImportProcessor)
        logger.info('Registered material processor.')

    def _process_material(self, material_id: str):
        logger.info(f"Material id is {str(material_id)}")
        with self.process_resource(RawMaterial, material_id):
            logger.info(f"Processed material id: {material_id}")

    def _bulk_process_material(self, material_ids: List[str]):
        with self.process_resource(DynamicsMaterialBulkPlaceholder, material_ids) as success:
            logger.info(f"Bulk processed {len(material_ids)} materials")
            return success

    def check_custom_table_exists(self):
        logger.info("We're creating a dictionary.")
        self.header_dict = {
            self.materials_table_name: {
                'No': '',
                'Description': '',
                'Type': 'Inventory',
                'Production_BOM_No': '',
                'Routing_No': '',
                'Quantity_on_Hand': 0,
                'Substitutes_Exist': 'FALSE',
                'Assembly_BOM': 'FALSE',
                'Vendor_Item_No': '',
                'Base_Unit_of_Measure': 'PCS',
                'Cost_is_Adjusted': 'TRUE',
                'Unit_Cost': 0,
                'Unit_Price': 0,
                'Vendor_No': '',
                'Default_Deferral_Template': '',
                'Inventory_Value_Zero': 'FALSE'
            },
            self.coating_items_table_name: {
                'No': '',
                'Description': '',
                'Search_Description': '',
                'Base_Unit_of_Measure': 'PCS',
                'Type': 'Inventory',
                'Inventory_Posting_Group': 'DEFAULT',
                'Unit_Price': 0,
                'Profit': 0,
                'Unit_Cost': 0,
                'Last_Direct_Cost': 0,
                'Indirect_Cost': 0,
                'Vendor_No': '',
                'Vendor_Item_No': '',
                'Lead_Time_Calculation': '',
                'Global_Dimension_1_Code': 0,
                'Global_Dimension_2_Code': 0,
                'Sales_Unit_of_Measure': 'PCS',
                'Purch_Unit_of_Measure': 'PCS',
                'Item_Category_Code': 0
            }
        }

        # add attributes as columns
        for pp_column_name, dynamics_name, default_value in Material.get_attributes():
            self.header_dict[self.materials_table_name][pp_column_name] = default_value
        for pp_column_name, dynamics_name, default_value in CoatingItem.get_attributes():
            self.header_dict[self.coating_items_table_name][pp_column_name] = default_value

        ImportCustomTable.check_custom_header_custom_table_exists(self.materials_table_name,
                                                                  self.header_dict[self.materials_table_name], 'No')
        ImportCustomTable.check_custom_header_custom_table_exists(self.coating_items_table_name,
                                                                  self.header_dict[self.coating_items_table_name], 'No')


class DynamicsMachineCenterImporter(WorkCenterImporter, DynamicsImporter):
    config_name = 'work_centers'
    table_name = 'workcenters'

    def _register_listener(self):
        self.listener = DynamicsImportListener(self._integration, 'import_work_center', MachineCenter)

    def _register_default_processors(self):
        self.register_processor(MachineCenter, DynamicsMachineCenterImportProcessor)
        self.register_processor(MachineCenterBulkPlaceholder, DynamicsMachineCenterBulkImportProcessor)

    def check_custom_table_exists(self):
        logger.info("We're creating a dictionary.")
        self.header_dict = {
            'No': '',
            'Name': '',
            'Work_Center_No': '',
            'Capacity': 0,
            'Efficiency': 100,
            'Search_Name': '',
            'Overhead_Rate': 0
        }
        ImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict, 'No')

    def _process_work_center(self, work_center_id: str):
        logger.info(f"Machine center id is {work_center_id}")
        with self.process_resource(MachineCenter, work_center_id):
            logger.info(f"Processed machine center id: {work_center_id}")

    def _bulk_process_work_center(self, work_center_ids: List[str]):
        with self.process_resource(MachineCenterBulkPlaceholder, work_center_ids) as success:
            logger.info(f"Bulk processed {len(work_center_ids)} machine centers")
            return success

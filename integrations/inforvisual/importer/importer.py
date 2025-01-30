from typing import List

from baseintegration.datamigration import logger
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.importer.material_importer import MaterialImporter
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from baseintegration.utils.custom_table import ImportCustomTable
from inforvisual.importer.configuration import InforVisualMaterialConfig, InforVisualPurchasedComponentConfig
from inforvisual.models import Customer, Part, PurchaseOrder
from inforvisual.importer.processors.account import AccountImportProcessor
from inforvisual.importer.processors.purchased_component import PurchasedComponentImportProcessor, \
    PurchasedComponentBulkPlaceholder, PurchasedComponentBulkImportProcessor
from inforvisual.importer.processors.material import MaterialImportProcessor, MaterialBulkPlaceholder, \
    MaterialBulkImportProcessor
from paperless.objects.customers import Account
from paperless.objects.purchased_components import PurchasedComponent
from django.db.models import Q
from paperless.objects.components import Material
from baseintegration.utils import get_last_action_datetime_sql


class InforVisualAccountImportListener:

    def __init__(self, integration):
        self.identifier = "import_account"
        self._integration = integration
        logger.info("Infor Visual account import listener was instantiated")

    def get_new(self, bulk=False):
        logger.info("Checking for new accounts")
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        updated_customers_query_set = Customer.objects.filter(modify_date__gt=date_to_search)
        logger.info(f"Found {str(updated_customers_query_set.count())} records to update")
        return updated_customers_query_set.values_list('id', flat=True)


class InforVisualAccountImporter(AccountImporter):

    def _register_listener(self):
        self.listener = InforVisualAccountImportListener(self._integration)
        logger.info("Infor Visual account listener was registered")

    def _register_default_processors(self):
        self.register_processor(Account, AccountImportProcessor)

    def _process_account(self, account_id: str):  # noqa: C901
        logger.info(f"Account id is {str(account_id)}")
        with self.process_resource(Account, account_id):
            logger.info(f"Account id {str(account_id)} was processed!")


class InforVisualMaterialImportListener:

    def __init__(self, integration):
        self.identifier = "import_material"
        self._integration = integration

        if self._integration.test_mode:
            config_dict = {}
        else:
            config_dict = self._integration.config_yaml["Importers"]["materials"]
        self.erp_config = InforVisualMaterialConfig(config_dict)

        logger.info("Infor Visual material import listener was instantiated")

    def get_new(self, bulk=False):
        logger.info("Getting new materials")
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)

        updated_query_set = Part.objects.\
            filter(Q(modify_date__gt=date_to_search) | Q(create_date__gt=date_to_search)).\
            filter(**self.erp_config.filter).exclude(**self.erp_config.exclude)
        return updated_query_set.values_list('id', flat=True)


class InforVisualMaterialImporter(MaterialImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "materials"
        else:
            self.table_name = "inforvisual_materials"

        if self._integration.test_mode:
            config_dict = {}
        else:
            config_dict = self._integration.config_yaml["Importers"]["materials"]
        self.erp_config = InforVisualMaterialConfig(config_dict)

    def _register_listener(self):
        self.listener = InforVisualMaterialImportListener(self._integration)
        logger.info("Infor Visual material listener was registered")

    def check_custom_table_exists(self):
        logger.info("We're creating a dictionary.")
        self.header_dict = {}
        for column_data in self.erp_config.imported_columns:
            column_name = column_data['column_name']
            default_value = column_data['default']
            self.header_dict[column_name] = default_value
        return ImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict,
                                                                         "material_id")

    def _register_default_processors(self):
        self.register_processor(Material, MaterialImportProcessor)
        self.register_processor(MaterialBulkPlaceholder, MaterialBulkImportProcessor)

    def _process_material(self, material_id: str):  # noqa: C901
        logger.info(f"Processing material with ID {material_id}")
        with self.process_resource(Material, material_id):
            logger.info(f"Processed material {str(material_id)}")

    def _bulk_process_material(self, material_ids: List[str]):
        with self.process_resource(MaterialBulkPlaceholder, material_ids) as success:
            logger.info(f"Bulk processed {len(material_ids)} materials")
            return success


class InforVisualPurchasedComponentImportListener:

    def __init__(self, integration):
        self.identifier = "import_purchased_component"
        self._integration = integration

        if self._integration.test_mode:
            config_dict = {}
        else:
            config_dict = self._integration.config_yaml["Importers"]["purchased_components"]
        self.erp_config = InforVisualPurchasedComponentConfig(config_dict)

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)

        if self.erp_config.import_from_purchase_orders:
            updated_query_set = PurchaseOrder.objects.filter(order_date__gt=date_to_search)
        else:
            updated_query_set = Part.objects.filter(
                Q(modify_date__gt=date_to_search) | Q(create_date__gt=date_to_search))\
                .filter(**self.erp_config.filter).exclude(**self.erp_config.exclude)

        return updated_query_set.values_list('id', flat=True)


class InforVisualPurchasedComponentImporter(PurchasedComponentImporter):

    def _register_listener(self):
        self.listener = InforVisualPurchasedComponentImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(PurchasedComponent, PurchasedComponentImportProcessor)
        self.register_processor(PurchasedComponentBulkPlaceholder, PurchasedComponentBulkImportProcessor)

    def _process_purchased_component(self, purchased_component_id: str):  # noqa: C901
        logger.info(f"Purchased component id is {str(purchased_component_id)}")
        with self.process_resource(PurchasedComponent, purchased_component_id):
            logger.info(f"Purchased component {str(purchased_component_id)} was processed")

    def _bulk_process_purchased_component(self, purchased_component_ids: List[str]):
        with self.process_resource(PurchasedComponentBulkPlaceholder, purchased_component_ids) as success:
            logger.info(f"Bulk processed {len(purchased_component_ids)} purchased components")
            return success

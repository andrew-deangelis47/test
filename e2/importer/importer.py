from typing import List
from django.db.models import Q
from baseintegration.datamigration import logger
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.importer.material_importer import MaterialImporter
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from baseintegration.importer.vendor_importer import VendorImporter
from baseintegration.importer.work_center_importer import WorkCenterImporter
from e2.importer.processors.vendor import VendorImportProcessor, VendorBulkPlaceholder, VendorBulkImportProcessor
from e2.importer.processors.workcenter import WorkCenterImportProcessor, WorkCenterBulkPlaceholder, \
    WorkCenterBulkImportProcessor
from paperless.objects.customers import Account
from paperless.objects.components import PurchasedComponent
from paperless.objects.components import Material
from e2.importer.processors.account import AccountImportProcessor
from e2.importer.processors.material import MaterialImportProcessor, MaterialBulkPlaceholder, \
    MaterialBulkImportProcessor
from e2.importer.processors.purchased_component import PurchasedComponentImportProcessor, \
    PurchasedComponentBulkPlaceholder, PurchasedComponentBulkImportProcessor
from e2.models import CustomerCode, Estim, Shipto, Contacts, Workcntr, Vendcode
from e2.utils import get_version_number
from e2.importer.configuration import CustomerImportConfig
from baseintegration.utils.custom_table import ImportCustomTable
from baseintegration.utils import get_last_action_datetime_sql


class E2AccountImportListener:

    def __init__(self, integration):
        self.identifier = "import_account"
        self._integration = integration
        logger.info("E2 account import listener was instantiated")

    def get_new(self, bulk=False):
        customer_codes = set()
        logger.info("Checking for new accounts")
        if get_version_number() == "default":
            date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)

            updated_customers_query_set = CustomerCode.objects.filter(Q(last_mod_date__gt=date_to_search) | Q(enterdate__gt=date_to_search))

            for customer_code in updated_customers_query_set.values_list('customer_code', flat=True):
                customer_codes.add(customer_code)

            updated_ship_to_query_set = Shipto.objects.filter(lastmoddate__gt=date_to_search)
            for customer_code in updated_ship_to_query_set.values_list('custcode', flat=True):
                customer_codes.add(customer_code)

            updated_contacts_query_set = Contacts.objects.filter(last_mod_date__gt=date_to_search)
            for customer_code in updated_contacts_query_set.values_list('code', flat=True):
                customer_codes.add(customer_code)
        else:
            updated_customers_query_set = CustomerCode.objects.all()
            for customer_code in updated_customers_query_set.values_list('customer_code', flat=True):
                customer_codes.add(customer_code)

            updated_ship_to_query_set = Shipto.objects.all()
            for customer_code in updated_ship_to_query_set.values_list('custcode', flat=True):
                customer_codes.add(customer_code)

            updated_contacts_query_set = Contacts.objects.all()
            for customer_code in updated_contacts_query_set.values_list('code', flat=True):
                customer_codes.add(customer_code)

        # contacts can have no customers
        customer_codes.discard(None)
        logger.info(f"Found {len(customer_codes)} records to update")
        return customer_codes


class E2AccountImporter(AccountImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.erp_config = CustomerImportConfig(
                should_import_sold_to_address=self._integration.config_yaml["Importers"]["accounts"].get(
                    "should_import_sold_to_address", "True"),
                should_import_salesperson_for_account=self._integration.config_yaml["Importers"]["accounts"].get(
                    "should_import_salesperson_for_account", "True"),
                should_import_billing_address=self._integration.config_yaml["Importers"]["accounts"].get(
                    "should_import_billing_address", "True"),
                should_import_shipping_addresses=self._integration.config_yaml["Importers"]["accounts"].get(
                    "should_import_shipping_addresses", "True"),
                should_import_contacts=self._integration.config_yaml["Importers"]["accounts"].get(
                    "should_import_contacts", "True"),
                should_skip_incomplete_addresses=self._integration.config_yaml["Importers"]["accounts"].get(
                    "should_skip_incomplete_addresses", "True"),
                tax_exempt_code=self._integration.config_yaml["E2"].get("tax_exempt_code", "None"))
        else:
            self.erp_config = CustomerImportConfig(should_import_sold_to_address=True,
                                                   should_import_salesperson_for_account=True,
                                                   should_import_billing_address=True,
                                                   should_import_shipping_addresses=True,
                                                   should_import_contacts=True,
                                                   should_skip_incomplete_addresses=True,
                                                   tax_exempt_code="tax")

    def _register_listener(self):
        self.listener = E2AccountImportListener(self._integration)
        logger.info("E2 account listener was registered")

    def _register_default_processors(self):
        self.register_processor(Account, AccountImportProcessor)

    def _process_account(self, account_id: str):  # noqa: C901
        logger.info(f"Processing account with id {account_id}")
        with self.process_resource(Account, account_id):
            logger.info(f"Processed account {str(account_id)}")


class E2MaterialImportListener:

    def __init__(self, integration):
        self.identifier = "import_material"
        self._integration = integration
        logger.info("E2 material import listener was instantiated")

    def check_custom_table_exists(self):
        return ImportCustomTable.check_custom_table_exists("materials", Estim, "partno")

    def get_new(self, bulk=False):
        logger.info("Checking for new materials")
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier,
                                                      bulk=bulk)
        codes_to_include = self._integration.config_yaml["Importers"]["materials"].get("codes_to_include", [])
        codes_to_exclude = self._integration.config_yaml["Importers"]["materials"].get("codes_to_exclude", [])
        updated_query_set = self.get_query_set(codes_to_exclude, codes_to_include, date_to_search)
        logger.info(f"Found {str(updated_query_set.count())} records to update")
        return updated_query_set.values_list('partno', flat=True)

    def get_query_set(self, codes_to_exclude, codes_to_include, date_to_search):
        if get_version_number() == "default":
            updated_query_set = Estim.objects.filter(lastmoddate__gt=date_to_search).exclude(
                vendcode1__isnull=True).exclude(vendcode1__exact='').filter(active__exact='Y')
        else:
            updated_query_set = Estim.objects.exclude(
                vendcode1__isnull=True).exclude(vendcode1__exact='').filter(active__exact='Y')
        if codes_to_include:
            updated_query_set = updated_query_set.filter(prodcode__in=codes_to_include)
        if codes_to_exclude:
            updated_query_set = updated_query_set.exclude(prodcode__in=codes_to_exclude)
        return updated_query_set


class E2MaterialImporter(MaterialImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "materials"
        else:
            self.table_name = "e2_materials"

    def _register_listener(self):
        self.listener = E2MaterialImportListener(self._integration)
        logger.info("E2 material listener was registered")

    def check_custom_table_exists(self):
        ImportCustomTable.check_custom_table_exists(self.table_name, Estim, "partno")

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


class E2PurchasedComponentListener:

    def __init__(self, integration):
        self.identifier = "import_purchased_component"
        self._integration = integration
        logger.info("E2 purchased component import listener was instantiated")

    def get_new(self, bulk=False):
        logger.info("Checking for new purchased components")
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier,
                                                      bulk=bulk)
        codes_to_include = self._integration.config_yaml["Importers"]["purchased_components"].get("codes_to_include",
                                                                                                  [])
        codes_to_exclude = self._integration.config_yaml["Importers"]["purchased_components"].get("codes_to_exclude",
                                                                                                  [])
        updated_query_set = self.get_query_set(codes_to_exclude, codes_to_include, date_to_search)
        logger.info(f"Found {str(updated_query_set.count())} records to update")
        return updated_query_set.values_list('partno', flat=True)

    def get_query_set(self, codes_to_exclude, codes_to_include, date_to_search):
        """ Separate this out as a helper function so it can be overridden if necessary. """
        if get_version_number() == "default":
            updated_query_set = Estim.objects.filter(lastmoddate__gt=date_to_search).exclude(
                vendcode1__isnull=True).exclude(vendcode1__exact='').filter(active__exact='Y')
        else:
            updated_query_set = Estim.objects.exclude(
                vendcode1__isnull=True).exclude(vendcode1__exact='').filter(active__exact='Y')
        if codes_to_include:
            updated_query_set = updated_query_set.filter(prodcode__in=codes_to_include)
        if codes_to_exclude:
            updated_query_set = updated_query_set.exclude(prodcode__in=codes_to_exclude)
        return updated_query_set


class E2PurchasedComponentImporter(PurchasedComponentImporter):

    def _register_listener(self):
        self.listener = E2PurchasedComponentListener(self._integration)
        logger.info("E2 purchased component listener was registered")

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


class E2WorkCenterImportListener:

    def __init__(self, integration):
        self.identifier = "import_work_center"
        self._integration = integration
        logger.info("E2 Work Center import listener was instantiated")

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier,
                                                      bulk=bulk)
        updated_query_set = self.get_query_set(date_to_search)
        return updated_query_set.values_list('workcntr', flat=True)

    def get_query_set(self, date_to_search):
        if get_version_number() == "default":
            updated_query_set = Workcntr.objects.filter(lastmoddate__gt=date_to_search).filter(active__exact='Y')
        else:
            updated_query_set = Workcntr.objects.filter(active__exact='Y')
        return updated_query_set


class E2WorkCenterImporter(WorkCenterImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "workcenters"
        else:
            self.table_name = "e2_workcenters"

    def _register_listener(self):
        self.listener = E2WorkCenterImportListener(self._integration)
        logger.info("E2 work center listener was registered")

    def _register_default_processors(self):
        self.register_processor(Workcntr, WorkCenterImportProcessor)
        self.register_processor(WorkCenterBulkPlaceholder, WorkCenterBulkImportProcessor)
        logger.info('Registered work center processor.')

    def check_custom_table_exists(self):
        logger.info("We're creating a dictionary.")
        self.header_dict = {
            'WorkCntr': 0,
            'ShortName': "",
            'Descrip': "",
            'BurdenRate': 0,
            'LaborRate': 0,
            'Cycle1': 0,
            'Setup1': 0,
            'LastModDate': ""
        }
        return ImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict,
                                                                         "WorkCntr")

    def _process_work_center(self, work_center_id: str):
        logger.info(f"Work center id is {str(work_center_id)}")
        with self.process_resource(Workcntr, work_center_id):
            logger.info(f"Processed work center id: {work_center_id}")

    def _bulk_process_work_center(self, work_center_ids: List[str]):
        with self.process_resource(WorkCenterBulkPlaceholder, work_center_ids) as success:
            logger.info(f"Bulk processed {len(work_center_ids)} work centers")
            return success


class E2VendorImportListener:

    def __init__(self, integration):
        self.identifier = "import_vendor"
        self._integration = integration
        logger.info("E2 Vendor import listener was instantiated")

    def get_new(self, bulk=False):
        date_to_search = get_last_action_datetime_sql(self._integration.managed_integration_uuid, self.identifier,
                                                      bulk=bulk)
        updated_query_set = self.get_query_set(date_to_search)
        return updated_query_set.values_list('vendcode', flat=True)

    def get_query_set(self, date_to_search):
        if get_version_number() == "default":
            updated_query_set = Vendcode.objects.filter(lastmoddate__gt=date_to_search).filter(active__exact='Y')
        else:
            updated_query_set = Vendcode.objects.filter(active__exact='Y')
        return updated_query_set


class E2VendorImporter(VendorImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            self.table_name = "vendors"
        else:
            self.table_name = "e2_vendors"

    def _register_listener(self):
        self.listener = E2VendorImportListener(self._integration)
        logger.info("E2 Vendor listener was registered")

    def _register_default_processors(self):
        self.register_processor(Vendcode, VendorImportProcessor)
        self.register_processor(VendorBulkPlaceholder, VendorBulkImportProcessor)
        logger.info('Registered vendor processor.')

    def check_custom_table_exists(self):
        logger.info("We're creating a dictionary.")
        self.header_dict = {
            'VendCode': "",
            'VendName': "",
            'VendType': "",
            'OutServ': "",
            'MinOrder': 0,
            'LeadTime': 0,
            'LastModDate': ""
        }
        return ImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict,
                                                                         "VendCode")

    def _process_vendor(self, vendor_id: str):
        logger.info(f"Vendor id is {str(vendor_id)}")
        with self.process_resource(Vendcode, vendor_id):
            logger.info(f"Processed vendor id: {vendor_id}")

    def _bulk_process_vendor(self, vendor_ids: List[str]):
        with self.process_resource(VendorBulkPlaceholder, vendor_ids) as success:
            logger.info(f"Bulk processed {len(vendor_ids)} vendors")
            return success

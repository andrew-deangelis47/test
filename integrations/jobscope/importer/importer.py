from typing import List

from baseintegration.datamigration import logger
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.importer.purchased_component_importer import PurchasedComponentImporter
from paperless.objects.customers import Account
from paperless.objects.components import PurchasedComponent
from jobscope.client import JobscopeClient
from jobscope.importer.processors.account import AccountImportProcessor
from jobscope.importer.processors.purchased_component import PurchasedComponentImportProcessor

from integrations.jobscope.importer.processors.purchased_component import PurchasedComponentBulkPlaceholder, \
    PurchasedComponentBulkImportProcessor


class JobscopeAccountImportListener:

    def __init__(self, integration, account_importer):
        self.identifier = "import_account"
        self._integration = integration
        self._account_importer = account_importer
        logger.info("Jobscope account import listener was instantiated")

    def get_new(self, bulk=False):
        self._account_importer._setup_erp_config()
        customers = self._integration.api_client.get_customers()
        customers_to_process = []
        for jobscope_acct in customers:
            if jobscope_acct.get("customerName") and jobscope_acct.get("customerNumber"):
                customers_to_process.append(jobscope_acct.get("customerNumber"))
        return customers_to_process


class JobscopeAccountImporter(AccountImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            api_url = self._integration.config_yaml["Jobscope"]["api_url"]
            self.client = JobscopeClient(api_url)
            username = self._integration.config["jobscope_username"]
            password = self._integration.config["jobscope_password"]
        else:
            self.client = JobscopeClient("http://testapi.com")
            username = "test"
            password = "test"
        self.client.login(username, password)
        self._integration.api_client = self.client

    def _register_listener(self):
        self.listener = JobscopeAccountImportListener(self._integration, self)
        logger.info("Jobscope account listener was registered")

    def _register_default_processors(self):
        self.register_processor(Account, AccountImportProcessor)

    def _process_account(self, account_id: str):  # noqa: C901
        with self.process_resource(Account, account_id):
            logger.info(f"Account id {str(account_id)} was processed!")


class JobscopePurchasedComponentImportListener:

    def __init__(self, integration, purchased_component_importer):
        self.identifier = "import_purchased_component"
        self._integration = integration
        self._purchased_component_importer = purchased_component_importer

    def get_new(self, bulk=False):
        self._purchased_component_importer._setup_erp_config()
        parts = self._integration.api_client.get_parts()
        parts_to_process = []
        for part in parts:
            mat_code = part.get("materialCostCategoryCode")
            if mat_code == "HARDWARE" or mat_code == "MECHANICAL":
                parts_to_process.append(part.get("partNumber"))
            else:
                continue
        return parts_to_process


class JobscopePurchasedComponentImporter(PurchasedComponentImporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            api_url = self._integration.config_yaml["Jobscope"]["api_url"]
            self.client = JobscopeClient(api_url)
            username = self._integration.config["jobscope_username"]
            password = self._integration.config["jobscope_password"]
        else:
            self.client = JobscopeClient("http://testapi.com")
            username = "test"
            password = "test"
        self.client.login(username, password)
        self._integration.api_client = self.client

    def _register_listener(self):
        self.listener = JobscopePurchasedComponentImportListener(self._integration, self)

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

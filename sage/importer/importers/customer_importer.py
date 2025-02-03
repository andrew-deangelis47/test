from baseintegration.importer.account_importer import AccountImporter
from sage.importer.importer import SageImporter
from sage.importer.listeners.customer import SageCustomerImportListener
from sage.models.sage_models.customer import Customer as SageCustomer
from sage.importer.processors.customer import SageCustomerImportProcessor, SageBulkCustomerImportProcessor, SageCustomerBulkPlaceholder
from baseintegration.datamigration import logger
from typing import List
from sage.importer.configuration import SageAccountConfig


class SageCustomerImporter(AccountImporter, SageImporter):

    def _register_listener(self):
        self.listener = SageCustomerImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(SageCustomer, SageCustomerImportProcessor)
        self.register_processor(SageCustomerBulkPlaceholder, SageBulkCustomerImportProcessor)
        logger.info('Registered customer processor.')

    def _process_account(self, customer_id: str):  # noqa: C901
        logger.info(f"Customer id is {str(customer_id)}")
        with self.process_resource(SageCustomer, customer_id):
            logger.info(f"Processed customer id: {customer_id}")

    def _bulk_process_accounts(self, customer_ids: List[str]):  # noqa: C901
        with self.process_resource(SageCustomerBulkPlaceholder, customer_ids) as success:
            logger.info(f"Bulk processed {len(customer_ids)} raw materials")
            return success

    def _setup_erp_config(self):
        self.erp_config = SageAccountConfig(self._integration.config_yaml)

from baseintegration.datamigration import logger
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.utils.custom_table import ImportCustomTable
from plex.configuration import ERPConfigFactory
from plex.objects.customer import Customer
from plex.importer.processors.accounts import AccountImportProcessor
from datetime import datetime


class PLEXAccountListener:
    identifier = "account_import"

    def __init__(self, integration, erp_config):
        self._integration = integration
        self._erp_config = erp_config

    def get_new(self, bulk=False):
        get_last_processed_date = ImportCustomTable.get_last_processed_date(self.identifier)
        existing_customers = Customer.find_customers()
        customer_codes = []
        now: str = datetime.now().isoformat()
        for customer in existing_customers:
            if customer.status in self._erp_config.import_customer_status_include_filter:
                customer_date: str = now
                if customer.modifiedDate is not None and customer.modifiedDate != '':
                    customer_date = customer.modifiedDate
                elif customer.createdDate is not None and customer.createdDate != '':
                    customer_date = customer.createdDate

                modified_date = datetime.fromisoformat(customer_date.replace('Z', ''))  # Zulu Timestamp conversion
                if modified_date > get_last_processed_date:
                    customer_codes.append(customer.code)
                else:
                    logger.debug(f'Skipping {customer.code} - old modified date, {customer.modifiedDate}')
            else:
                logger.debug(f'Skipping {customer.code} - status filter exclusion, current status {customer.status}')

        ImportCustomTable.update_last_processed_date(self.identifier)
        return customer_codes


class PLEXAccountImporter(AccountImporter):

    def _setup_erp_config(self):
        logger.info("setting up erp config")
        self.erp_config, self.plex_client = ERPConfigFactory.create_config(self._integration)

    def _register_default_processors(self):
        self.register_processor(Customer, AccountImportProcessor)

    def _register_listener(self):
        self.listener = PLEXAccountListener(self._integration, self.erp_config)

    def _process_account(self, account_id: str):
        self._setup_erp_config()
        logger.info(f"Processing Account: {str(account_id)}")
        with self.process_resource(Customer, account_id) as result:
            return result

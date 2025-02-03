from baseintegration.datamigration import logger
from plex_v2.objects.customer import Customer
from datetime import datetime
from integrations.baseintegration.utils import get_last_action_datetime
from pendulum.datetime import DateTime


class PLEXAccountListener:
    identifier = "account_import"

    def __init__(self, integration, erp_config):
        self._integration = integration
        self._erp_config = erp_config

    def get_new(self, bulk=False):
        last_processed_date = get_last_action_datetime(self._integration.managed_integration_uuid, self.identifier, bulk=bulk)
        existing_customers = Customer.find_customers()
        customer_codes = []
        now: str = datetime.now().isoformat()
        for customer in existing_customers:

            # check that it was updated since the last run
            if self._was_updated_since_last_run(customer, last_processed_date, now):
                # check if the status is valid
                if self._is_valid_status(customer):
                    customer_codes.append(customer.code)

        return customer_codes

    def _is_valid_status(self, customer: Customer) -> bool:
        if customer.status not in self._erp_config.import_customer_status_include_filter:
            logger.debug(f'Skipping {customer.code} - status filter exclusion, current status is {customer.status}')
            return False
        return True

    def _was_updated_since_last_run(self, customer: Customer, last_action_date: DateTime, now: str) -> bool:
        material_update_date: str = now
        if customer.modifiedDate is not None and customer.modifiedDate != '':
            material_update_date = customer.modifiedDate
        elif customer.createdDate is not None and customer.createdDate != '':
            material_update_date = customer.createdDate

        modified_date = datetime.fromisoformat(material_update_date.replace('Z', ''))  # Zulu Timestamp conversion

        if modified_date <= last_action_date:
            logger.debug(f'Skipping {customer.code} - old modified date, {customer.modifiedDate}')

        return modified_date > last_action_date

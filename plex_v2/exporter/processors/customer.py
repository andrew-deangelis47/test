from paperless.objects.orders import OrderAccount
from plex_v2.objects.customer import Customer
from baseintegration.datamigration import logger
from plex_v2.exporter.processors.base import PlexProcessor
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex_v2.factories.plex.customer import PlexCustomerFactory
from plex_v2.utils.export import ExportUtils


class CustomerProcessor(PlexProcessor):
    """
    Gets the customer in Plex based on the contact on the order
    If configured it will create the customer in Plex if it is not found
    """

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'customer'

    def _process(self, account: OrderAccount, utils: ExportUtils, customer_factory: PlexCustomerFactory) -> Customer:

        # 1) get existing customer in Plex
        existing_customer_in_plex: Customer = utils.get_plex_customer_by_code_or_name(account)

        # 2) if one does not exist, and we are not configured to create customer then exit
        if not existing_customer_in_plex and not self.config.can_creat_new_customers:
            logger.info('Customer does not exist in Plex and creation is disabled. Will not export')
            self._add_report_message('Customer does not exist in Plex and creation is disabled. Will not export')
            raise CancelledIntegrationActionException('Customer does not exist in Plex and creation is disabled. Will not export')

        # 2) if one does not exist, and we are configured to create customer then create it
        if not existing_customer_in_plex and self.config.can_creat_new_customers:
            self._add_report_message('Creating new customer with code {} and name {}'.format(account.erp_code, account.name))
            logger.info('Creating new customer with code {} and name {}'.format(account.erp_code, account.name))
            new_customer = customer_factory.to_plex_customer(account)
            return new_customer.create()

        # 3) if the existing customer has a valid status, return it
        if existing_customer_in_plex and existing_customer_in_plex.status != 'Deleted':
            logger.info(f'Using existing customer: {existing_customer_in_plex.code}')
            self._add_report_message(f'Using existing customer: {existing_customer_in_plex.code}')
            return existing_customer_in_plex

        logger.info(f'Customer exists but does not have a valid status "{existing_customer_in_plex.name}". Will not export')
        self._add_report_message(f'Customer exists but does not have a valid status "{existing_customer_in_plex.name}". Will not export')
        raise CancelledIntegrationActionException(f'Customer exists but does not have a valid status "{existing_customer_in_plex.name}". Will not export')

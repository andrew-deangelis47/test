from typing import Optional
from typing import Union
from paperless.exceptions import PaperlessNotFoundException
from paperless.objects.quotes import Quote
from paperless.objects.orders import Order
from paperless.objects.customers import Account
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from baseintegration.exporter import logger
from baseintegration.exporter.processor import BaseProcessor
from sage.sage_api.client import SageImportClient
from sage.sage_api.filter_generation.customer_filter_generator import CustomerFilterGenerator
from sage.exporter.converters.paperless_account_to_sage_customer_i_file_converter import \
    PaperlessAccountToSageCustomerIFileConverter
from sage.models.sage_models.customer.customer_full_entity import SageCustomerFullEntity


def _get_customer_in_sage(paperless_account: Account) -> Optional[SageCustomerFullEntity]:
    """
    gets specified customer in sage
    """
    client = SageImportClient.get_instance()
    logger.info(f'Attempting to match account with ID {paperless_account.erp_code}')
    return client.get_resource(SageCustomerFullEntity,
                               CustomerFilterGenerator.get_filter_by_id(paperless_account.erp_code), False)


def _get_paperless_account(quote: Quote) -> Account:
    """
    gets paperless account from the order contact
    """
    if quote.contact.account and quote.contact.account.id:
        try:
            return Account.get(quote.contact.account.id)
        except PaperlessNotFoundException:
            raise CancelledIntegrationActionException(f'Paperless Parts Account does not exist for contact: '
                                                      f'"{quote.contact.first_name} {quote.contact.last_name}". '
                                                      f'Missing Account name: "{quote.contact.account.name}"; '
                                                      f'ERP Code: "{quote.contact.account.erp_code}"')
    else:
        raise CancelledIntegrationActionException(f'Order contact {quote.contact.email} '
                                                  f'does not have associated Paperless Parts Account.')


def _create_customer_in_sage(paperless_account: Account) -> SageCustomerFullEntity:
    """
    creates customer in sage
    """
    i_file = PaperlessAccountToSageCustomerIFileConverter.to_sage_customer_i_file(paperless_account)
    client = SageImportClient.get_instance()
    client.create_customer(i_file)
    logger.info('creating customer in sage: ' + paperless_account.name)


class CustomerProcessor(BaseProcessor):
    def _process(self, order: Order) -> Union[SageCustomerFullEntity, None]:
        """
        Process a customer from PaperlessParts into Sage. Checks to see if
        the customer exists, otherwise creates the customer from account data
        """

        logger.info('PROCESSING THE CUSTOMER')

        quote = Quote.get(order.quote_number, order.quote_revision_number)

        # 0) get the paperless account
        paperless_account = _get_paperless_account(quote)

        # 1) get the sage customer associated with the paperless account
        sage_customer = _get_customer_in_sage(paperless_account)

        # 2A) if we have this account (customer) in sage, then we do nothing
        if sage_customer is not None:
            logger.info('Customer was found! Id ' + sage_customer.customer.code)
            return sage_customer

        # 2B) if we don't find this account in sage, stop processing
        logger.info('Customer was not found... cannot export order without the customer existing in Sage')
        logger.info('If the customer exists in Sage, the customer import must run then this order will be able to be exported')

        return None

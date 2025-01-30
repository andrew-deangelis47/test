from plex_v2.configuration import PlexConfig
from plex_v2.objects.customer import Customer
from paperless.objects.customers import Account
from plex_v2.objects.payment_terms_mapping import PaymentTermsMappingList
from plex_v2.objects.customers_api_get import CustomersApiGet
from typing import Union, List
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from paperless.exceptions import PaperlessException
from baseintegration.datamigration import logger


class AccountFactory:

    def __init__(self, config: PlexConfig):
        self.config: PlexConfig = config

    def to_paperless_account(self, plex_customer: Customer, payment_terms_mapping_list: Union[PaymentTermsMappingList, None]) -> Account:
        account: Account = Account(
            name=plex_customer.name,
            erp_code=plex_customer.code,
            notes=plex_customer.note,
            payment_terms=self.config.default_payment_terms,
            payment_terms_period=self.config.default_payment_terms_period
        )

        # # set the payment terms if configured
        if payment_terms_mapping_list is not None:
            # if the payment terms are not in the table then we still want to continue
            try:
                payment_terms, payment_terms_period = self.get_payment_terms_and_period(plex_customer, payment_terms_mapping_list)
                account.payment_terms = payment_terms
                account.payment_terms_period = payment_terms_period
            except PaperlessException as e:
                logger.info(e)

        return account

    def get_payment_terms_and_period(self, plex_customer: Customer, payment_terms_mapping_list: PaymentTermsMappingList):
        # 1) get the terms
        customer_information: List[CustomersApiGet] = CustomersApiGet.get(plex_customer.code)
        if len(customer_information) == 0:
            raise CancelledIntegrationActionException(
                f'Could not get customer information from plex data source {CustomersApiGet.get_resource_name()}. Customer code is {plex_customer.code}')

        customer_information: CustomersApiGet = customer_information[0]
        payment_terms: str = customer_information.Terms

        # 2) use the mapping to get the terms period
        payment_terms_period: Union[int, float] = payment_terms_mapping_list._get_period_by_terms(payment_terms)
        if payment_terms_period is None:
            raise PaperlessException(
                f'No matching terms period found for payment terms "{payment_terms}". Please add the corresponding '
                f'payment term period in the "{self.config.payment_mapping_custom_table_name}" custom table.')

        return payment_terms, payment_terms_period

from plex_v2.objects.customer import Customer, CustomerContact
from paperless.objects.customers import Contact
from plex_v2.utils.import_utils import ImportUtils
from plex_v2.factories.paperless.account import AccountFactory
from plex_v2.factories.paperless.contact import ContactFactory
from plex_v2.importer.processors.base import PlexImportProcessor
from paperless.exceptions import PaperlessException
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex_v2.objects.payment_terms_mapping import PaymentTermsMappingList
from typing import Union
from baseintegration.datamigration import logger
from paperless.objects.customers import Account


class AccountImportProcessor(PlexImportProcessor):
    _fallback_country_alpha_3 = 'USA'
    PP_ERROR_ACCOUNT_NAME_ALREADY_EXISTS = 'This group already has an account with this name'

    def _process(self, account_id: str, utils: ImportUtils, account_factory: AccountFactory, contact_factory: ContactFactory, payment_terms_mapping_list: Union[PaymentTermsMappingList, None]):
        # 1) get the plex customer if it exists (will gracefully error out if not found)
        plex_customer: Customer = utils.get_plex_customer_by_code(account_id)

        # 2) get existing account if there is one
        pp_account: Account = utils.get_existing_pp_account(account_id)

        # 3) if there is no account create it
        if pp_account is None:
            pp_account = account_factory.to_paperless_account(plex_customer, payment_terms_mapping_list)

            # 3-A) handle if there is already an account with this name
            try:
                pp_account.create()
            except PaperlessException as e:
                if self.PP_ERROR_ACCOUNT_NAME_ALREADY_EXISTS not in str(e):
                    raise CancelledIntegrationActionException(str(e))

        # 4) if account exists, update the name and terms
        else:
            # TODO: should we make it configurable what properties we update?
            #       we will at least update the name and the terms

            pp_account.name = plex_customer.name

            # if the terms are not in the table then we still want to continue
            if self.config.should_import_customer_terms:
                try:
                    payment_terms, payment_period = account_factory.get_payment_terms_and_period(plex_customer, payment_terms_mapping_list)
                    pp_account.payment_terms = payment_terms
                    pp_account.payment_terms_period = payment_period
                except PaperlessException as e:
                    logger.info(e)

            pp_account.update()

        # 5) create contacts
        plex_contact: CustomerContact
        valid_plex_contacts = utils.get_and_validate_contacts(account_id)
        for plex_contact in valid_plex_contacts:
            logger.info(f'processing contact with email "{plex_contact.email}"')

            try:
                pp_contact: Contact = contact_factory.to_paperless_contact(plex_contact, pp_account.id)
                pp_contact.create()
            except PaperlessException as e:
                # handle if there is already a contact with that email
                if 'This group already has a contact with this email' in str(e):
                    logger.info(f'This group already has a contact with this email "{pp_contact.email}"')
                else:
                    raise e

        # 6) create addresses
        utils.create_address(
            plex_customer.id,
            pp_account,
            self._importer.erp_config.use_billing_address_prefix,
            self._importer.erp_config.should_use_address_code_for_facility_name
        )

        return True

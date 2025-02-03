from typing import Union

from baseintegration.utils import create_or_update_account
from paperless.exceptions import PaperlessException
from paperless.objects.customers import Account, Contact as PaperlessContact

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.exporter.order_exporter import logger

from dynamics.exceptions import DynamicsNotFoundException
from dynamics.importer.utils import PaperlessObjectCreator, DynamicsToPaperlessTranslator, ObjectMatchChecker
from dynamics.objects.customer import Customer, Contact


class AccountImportProcessor(BaseImportProcessor):

    def _process(self, account_id: str = None):
        self.import_customer(account_id)

    def import_customer(self, account_id: str = None):
        try:
            logger.info(f'Importing account {account_id}')

            dynamics_customer = Customer.get_first({'No': account_id})

            paperless_account, is_new_account = create_or_update_account(self._importer._integration, account_id,
                                                                         dynamics_customer.Name)
            if not is_new_account and ObjectMatchChecker.account_matches(dynamics_customer, paperless_account):
                logger.info(f"Account '{account_id}' exists and does not require update.")
            elif not dynamics_customer.Name or not dynamics_customer.Name.strip():
                logger.info(f"Account '{account_id}' exists but does not have a name - skipping")
                return
            else:
                DynamicsToPaperlessTranslator.update_account(paperless_account, dynamics_customer)
                if is_new_account:
                    self._create_new_paperless_account(paperless_account)
                else:
                    self._update_paperless_account(paperless_account)

            paperless_account_id = paperless_account.id

            logger.info(f'Importing contacts for account {account_id}')
            dynamics_contacts = Contact.get_all({
                'Company_Name': dynamics_customer.Name
            })
            for dynamics_contact in dynamics_contacts:
                dynamics_contact: Contact
                dynamics_contact_email = dynamics_contact.E_Mail
                if not dynamics_contact_email:
                    logger.warning(f'Contact {dynamics_contact.Name} does not have email, skipping import')
                    continue
                is_person = dynamics_contact.Type == 'Person'
                logger.info(f'Importing contact {dynamics_contact_email}')
                paperless_contact = self._get_paperless_contact(dynamics_contact_email)
                if paperless_contact:
                    if not is_person:
                        # do not overwrite first & last name for non-person contacts
                        dynamics_contact.First_Name = paperless_contact.first_name
                        dynamics_contact.Surname = paperless_contact.last_name

                    requires_update = not ObjectMatchChecker.contact_matches(dynamics_contact, paperless_contact,
                                                                             paperless_account_id)
                    if requires_update:
                        logger.info(f"Updating contact '{dynamics_contact_email}'")
                        self._update_paperless_contact(dynamics_contact, paperless_contact, paperless_account_id)
                    else:
                        logger.info(f"Contact '{dynamics_contact_email}' exists and does not require update.")
                else:
                    logger.info(f"Paperless contact '{dynamics_contact_email}' does not exist, creating")
                    if not is_person:
                        dynamics_contact.First_Name = 'Default'
                        dynamics_contact.Surname = 'Contact'
                    self._create_new_paperless_contact(dynamics_contact, paperless_account_id)
        except DynamicsNotFoundException:
            logger.info(f'Dynamics customer with ID {account_id} not found.')

    @staticmethod
    def _update_paperless_account(paperless_account: Account):
        try:
            paperless_account.update()
            logger.info(f"Updated account: {paperless_account.erp_code}")
        except PaperlessException as e:
            logger.warning(e)
            logger.warning(f"Failed to update account: {paperless_account.erp_code}")

    @staticmethod
    def _create_new_paperless_account(paperless_account: Account):
        try:
            paperless_account.create()
            logger.info(f"New account created: {paperless_account.erp_code}")
            return paperless_account
        except PaperlessException as e:
            logger.warning(f"Failed to create account: {paperless_account.erp_code}")
            raise e

    @staticmethod
    def _update_paperless_contact(dynamics_contact: Contact, paperless_contact: PaperlessContact,
                                  paperless_account_id: int):
        DynamicsToPaperlessTranslator.update_contact(paperless_contact, dynamics_contact, paperless_account_id)
        try:
            paperless_contact.update()
            logger.info(f"Updated contact: {paperless_contact.email}")
        except PaperlessException as e:
            logger.warning(e)
            logger.warning(f"Failed to update contact: {paperless_contact.email}")

    @staticmethod
    def _create_new_paperless_contact(dynamics_contact: Contact, paperless_account_id: int):
        paperless_contact = PaperlessObjectCreator.empty_contact()
        DynamicsToPaperlessTranslator.update_contact(paperless_contact, dynamics_contact, paperless_account_id)
        try:
            paperless_contact.create()
            logger.info(f"New contact created: {paperless_contact.email}")
        except PaperlessException as e:
            logger.warning(e)
            logger.warning(f"Failed to create contact: {paperless_contact.email}")

    @staticmethod
    def _get_paperless_contact(dynamics_contact_email: str) \
            -> Union[PaperlessContact, None]:
        pp_contacts_list = PaperlessContact.search(dynamics_contact_email)
        for pp_contact in pp_contacts_list:
            if pp_contact.email == dynamics_contact_email:
                return PaperlessContact.get(id=pp_contact.id)
        return None

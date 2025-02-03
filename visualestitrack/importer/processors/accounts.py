from baseintegration.importer.import_processor import BaseImportProcessor
from visualestitrack.models import Accounts, Facilities, Contacts
from paperless.objects.customers import AccountList, Account, Contact, Facility
from paperless.objects.address import Address
from paperless.objects.common import Money
from paperless.exceptions import PaperlessException

from baseintegration.datamigration import logger


class AccountImportProcessor(BaseImportProcessor):

    def _process(self, account_id: str):
        facilities = Facilities.objects.filter(estitrack_account_id=account_id)
        facility = facilities[0]
        vet_account: Accounts
        vet_account = Accounts.objects.filter(estitrack_account_id=facility.estitrack_account_id).first()
        if vet_account is None:
            logger.warning(f'Could not find account record in VET aborting account seeding to Paperless Parts '
                           f'- {account_id}')
            return False
        account = Account.filter(erp_code=account_id.strip())
        pp_account: Account = None

        if len(account) > 0:
            logger.info(f"VET Account found by ERP code match moving on to next account - {account_id}")
            return True

        if pp_account is None:
            pp_account_list: AccountList
            pp_account_list = AccountList.list()
            duplicate_name = False

            for account in pp_account_list:
                if str(facility.attention).strip() == str(account.name).strip():
                    if account.erp_code is not None:
                        duplicate_name = True
                        break
                    logger.info(f"Potential Account match found by name setting ERP code to: {account_id} on"
                                f" account: {account.id}")
                    pp_account = Account.get(id=account.id)
                    pp_account.erp_code = facility.estitrack_account_id
                    pp_account.update()
                    break

        if pp_account is None:
            logger.info(f"No match found, creating account in Paperless - {account_id}")
            if facility.attention is None or facility.attention.strip() == '':
                logger.warning(
                    f'Could not find account name aborting account seeding to Paperless Parts - {account_id}')
                return False
            account_name = facility.attention
            if duplicate_name:
                account_name = f'{account_id} - {account_name}'
            pp_account = Account(name=account_name)
            pp_account.erp_code = facility.estitrack_account_id
            pp_account.url = vet_account.url
            pp_account.notes = vet_account.notes
            pp_account.phone = vet_account.phone
            money: Money = Money(raw_amount=float(vet_account.credit_line))
            pp_account.credit_line = money
            pp_account.phone_ext = vet_account.phone_ext
            try:
                pp_account.create()
            except PaperlessException:
                logger.exception(f'An Unexpected Exception catch in AccountImportProcessor for account creation which '
                                 f'prevented creation for PP account: {account_id} ')
                return False
        if pp_account.payment_terms is None:
            self.set_payment_terms(account_id, vet_account, pp_account)
        if pp_account.sold_to_address is None:
            self.set_sold_to_address(account_id, vet_account, pp_account)
        self.create_contacts(account_id, pp_account.id)
        self.set_facility_addresses(account_id, facilities, pp_account)
        return True

    @staticmethod
    def set_payment_terms(account_id, vet_account: Accounts, pp_account: Account):
        period = 30
        raw_terms = vet_account.payment_terms.strip() if vet_account.payment_terms is not None else ''
        terms = raw_terms if raw_terms != '' else 'NET 30'
        pp_account.payment_terms = terms
        if "Days" in pp_account.payment_terms:
            period = ''.join(filter(str.isdigit, pp_account.payment_terms))
        pp_account.payment_terms_period = period
        try:
            pp_account.update()
        except PaperlessException as e:
            logger.warning(f'Exception catch in AccountImportProcessor while attempting account update for '
                           f'payment terms for PP account: {account_id} with message: {e.message}')

    @staticmethod
    def set_facility_addresses(account_id, facilities: [Facilities], pp_account: Account):
        if facilities is None:
            return

        for facility in facilities:
            pp_facility = Facility(account_id=pp_account.id, name=f'{facility.id} - {facility.name}')
            pp_facility.attention = facility.attention
            pp_facility.address: Address = Address(address1=facility.address1, address2=facility.address2,
                                                   city=facility.city, state=facility.state,
                                                   postal_code=facility.postal_code, country=facility.country)
            try:
                pp_facility.create(account_id=pp_account.id)
            except PaperlessException:
                logger.warning(f'Exception catch in AccountImportProcessor while attempting account update for '
                               f'VET facility ({facility.id}) address for VET account: {account_id} ')

    @staticmethod
    def set_sold_to_address(account_id, vet_account: Accounts, pp_account: Account):
        a_address: Address = Address(address1=vet_account.address1, address2=vet_account.address2,
                                     city=vet_account.city, state=vet_account.state,
                                     postal_code=vet_account.postal_code, country=vet_account.country)
        pp_account.sold_to_address = a_address
        try:
            pp_account.update()
        except PaperlessException:
            logger.warning(f'Exception catch in AccountImportProcessor while attempting account update for '
                           f'sold to address for PP account: {account_id} ')

    @staticmethod
    def create_contacts(vet_account_id, pp_account_id):
        vet_contacts = Contacts.objects.filter(customercode=vet_account_id)
        pp_contacts = Contact.filter(account_id=pp_account_id)
        for vet_contact in vet_contacts:
            email = vet_contact.email.strip()
            name = vet_contact.name.strip()
            if email is None or email == '':
                logger.warning(f"Email Address is missing cannot create contact '{name}' for {vet_account_id}")
                continue
            if name is None or name == '':
                logger.warning(f"Name is missing cannot create contact '{email}' for {vet_account_id}")
                continue
            for contact in pp_contacts:
                if contact.email == email:
                    logger.info('A contact with this email already exists for this account, skipping')
                    continue
            pp_contact = Contact(account_id=pp_account_id, first_name=name, last_name='.', email=email)
            vet_contact: Contacts
            pp_contact.notes = vet_contact.notes
            pp_contact.phone = vet_contact.phone
            pp_contact.phone_ext = vet_contact.phone_ext
            try:
                pp_contact.create()
            except PaperlessException as e:
                if 'Enter a valid email address' in e.message:
                    logger.warning(f'Email format issue found for: Name - {pp_contact.first_name}, '
                                   f'Email: {pp_contact.email}, Account: {pp_account_id} . Skipping contact creation')
                    continue
                if 'This group already has a contact with this email' in e.message:
                    logger.warning(f'The Email: {pp_contact.email} , is already being used on a different account '
                                   f'for this paperless parts customer. Skipping contact creation')
                    continue
                else:
                    logger.exception(f'An Unexpected Exception catch in AccountImportProcessor for contact creation '
                                     f'and we unable to create the contact for account: {vet_account_id}')
            c_address: Address = Address(address1=vet_contact.address1, address2=vet_contact.address2,
                                         city=vet_contact.city, state=vet_contact.state,
                                         postal_code=vet_contact.postal_code, country=vet_contact.country)
            pp_contact.address = c_address
            try:
                pp_contact.update()
            except PaperlessException:
                logger.warning('Exception catch in AccountImportProcessor while attempting to add contact address.')

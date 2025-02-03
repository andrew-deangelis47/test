import re

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.address import AddressUtils
from plex.objects.customer import Customer, CustomerContacts, CustomerAddress
from paperless.objects.customers import AccountList, Account, Contact, Facility, BillingAddress, Address
from paperless.exceptions import PaperlessException

from baseintegration.datamigration import logger


class AccountImportProcessor(BaseImportProcessor):
    _fallback_country_alpha_3 = 'USA'

    def _process(self, account_id: str):
        existing_customers = Customer.find_customers(code=account_id)
        existing_customer: Customer = existing_customers[0] if len(existing_customers) > 0 else None
        if existing_customer is None:
            logger.warning(f'Invalid Plex customer Code provided to importer: {account_id}')
            return False
        pp_accounts = Account.filter(erp_code=account_id)
        pp_account: Account = None
        if len(pp_accounts) < 1:

            name = existing_customer.name
            pp_accounts_by_name: AccountList = Account.search(search_term=name)
            for item in pp_accounts_by_name:
                if item.erp_code is None and item.name == name:
                    logger.info(f"Account {account_id} found by Name match - {name}")
                    pp_account = Account.get(id=item.id)
                    pp_account.erp_code = account_id
                    pp_account.update()
                    break
            if pp_account is None:
                number = len(pp_accounts_by_name)
                if number > 0:
                    name += f'-{number}'
                pp_account = Account(name=name, erp_code=account_id)
                pp_account.create()
        else:
            logger.info(f"Account {account_id} found by ERP code match")
            pp_account = Account.get(id=pp_accounts[0].id)
        pp_account.notes = existing_customer.note
        pp_account.update()

        self.create_contacts(existing_customer.id, pp_account.id)
        self.create_address(existing_customer.id, pp_account)

        return True

    def create_contacts(self, customer_id: str, pp_account_id: str):
        plex_contacts = CustomerContacts.find_customer_contacts(customer_id=customer_id)
        plex_contact: CustomerContacts
        pp_contacts = Contact.filter(account_id=pp_account_id)
        for plex_contact in plex_contacts:
            create = False
            if plex_contact.email is None or plex_contact.email.strip() == '':
                e_msg = f'{plex_contact.companyName}, Missing Email, {plex_contact.firstName} {plex_contact.lastName}'
                logger.debug(e_msg)
                logger.warning(f"Email Address is missing cannot create contact "
                               f"'{plex_contact.firstName} {plex_contact.lastName}' for {plex_contact.companyName}")
                continue

            pp_contact = None
            email = plex_contact.email.strip()
            for contact in pp_contacts:
                if contact.email == email:
                    pp_contact = Contact.get(id=contact.id)
                    break
            if pp_contact is None:
                create = True
                pp_contact = Contact(account_id=int(pp_account_id), first_name=plex_contact.firstName,
                                     last_name=plex_contact.lastName, email=email)
            pp_contact.notes = plex_contact.note
            pp_contact.phone = self.scrub_phone_number(plex_contact.phone)
            try:
                if create:
                    pp_contact.create()
                else:
                    pp_contact.update()
            except PaperlessException as e:
                if 'email' in e.message:
                    logger.warning(f'Email issue prevented contact {pp_contact.first_name} {pp_contact.last_name} '
                                   f'with email {pp_contact.email} from processing '
                                   f'for account: {plex_contact.companyName} with reason: {e.message}')
                elif 'last_name' in e.message:
                    logger.warning(
                        f'Missing last name issue prevented contact {pp_contact.first_name} {pp_contact.last_name} '
                        f'with email {pp_contact.email} from processing '
                        f'for account: {plex_contact.companyName} with reason: {e.message}')
                else:
                    logger.exception(f'An Unexpected Exception catch in AccountImportProcessor for contact creation '
                                     f'and we unable to create the contact for account: {plex_contact.companyName}')
                continue

    def create_address(self, plex_customer_id: str, pp_account: str):
        plex_locations: [CustomerAddress] = CustomerAddress.find_customer_addresses(
            code=None,
            billTo=None,
            remitTo=None,
            shipTo=None,
            soldTo=None,
            resource_name_kwargs={
                'customer_id': plex_customer_id
            }
        )
        pp_facilities = Facility.list(account_id=pp_account.id)
        pp_billings = BillingAddress.list(account_id=pp_account.id)
        for plex_location in plex_locations:
            country_alpha_3, state_province_name = AddressUtils.get_country_and_state(plex_location.country.strip(),
                                                                                      plex_location.state.strip(),
                                                                                      plex_location.zip[0:5].strip(),
                                                                                      self._fallback_country_alpha_3)
            if plex_location.billTo:
                self.add_billing(plex_customer_id, pp_account.id, plex_location, pp_billings, state_province_name,
                                 country_alpha_3)
            elif plex_location.soldTo:
                self.add_sold_to(plex_customer_id, pp_account, plex_location, state_province_name, country_alpha_3)
            else:
                self.add_facility(plex_customer_id, pp_account.id, plex_location, pp_facilities, state_province_name,
                                  country_alpha_3)

    @staticmethod
    def add_facility(plex_customer_id: str, pp_account_id: str, plex_location: CustomerAddress,
                     pp_facilities: [Facility], state_province_name: str, country_alpha_3: str):
        create = False
        pp_address = None
        name = plex_location.name
        for pp_facility in pp_facilities:
            if pp_facility.name == name:
                pp_address = Facility.get(id=pp_facility.id)
                break
        if pp_address is None:
            create = True
            pp_address = Facility(account_id=pp_account_id, name=name)
        pp_address.address = Address(address1=plex_location.address.strip(), city=plex_location.city.strip(),
                                     state=state_province_name, postal_code=plex_location.zip[0:5].strip(),
                                     country=country_alpha_3)
        try:
            if create:
                pp_address.create(account_id=pp_account_id)
            else:
                pp_address.update()
        except PaperlessException:
            f_msg = f' {plex_customer_id}, Invalid Facility Address, street:{pp_address.address.address1}  ' \
                    f'city:{pp_address.address.city} state:{state_province_name} ' \
                    f'zip:{pp_address.address.postal_code}  country:{pp_address.address.country}'
            logger.debug(f_msg)
            logger.warning(f'Exception catch in AccountImportProcessor while attempting to add '
                           f'Facility address: {plex_customer_id}-{plex_location.name}')

    @staticmethod
    def add_billing(plex_customer_id: str, pp_account_id: str, plex_location: CustomerAddress,
                    pp_billings: [BillingAddress], state_province_name: str, country_alpha_3: str):
        for pp_billing in pp_billings:
            if pp_billing.address1 == plex_location.address.strip() and \
                    pp_billing.city == plex_location.city.strip() and \
                    pp_billing.country == country_alpha_3 and pp_billing.state == state_province_name and \
                    pp_billing.postal_code == plex_location.zip[0:5].strip():
                return
        pp_address = BillingAddress(address1=plex_location.address.strip(), city=plex_location.city.strip(),
                                    state=state_province_name, postal_code=plex_location.zip[0:5].strip(),
                                    country=country_alpha_3)
        try:
            pp_address.create(account_id=pp_account_id)
        except PaperlessException:
            b_msg = f' {plex_customer_id}, Invalid Billing Address, street:{pp_address.address1} ' \
                    f'city:{pp_address.city} state:{pp_address.state} zip:{pp_address.postal_code} ' \
                    f'country:{pp_address.country}'
            logger.debug(b_msg)
            logger.warning(f'Exception catch in AccountImportProcessor while attempting to add '
                           f'Billing address: {plex_customer_id}-Billing-{plex_location.name}')

    @staticmethod
    def add_sold_to(plex_customer_id: str, pp_account: Account, plex_location: CustomerAddress,
                    state_province_name: str, country_alpha_3: str):
        pp_account

        a_account: Address = Address(address1=plex_location.address.strip(), city=plex_location.city.strip(),
                                     state=state_province_name, postal_code=plex_location.zip[0:5].strip(),
                                     country=country_alpha_3)
        pp_account.sold_to_address = a_account
        try:
            pp_account.update()
        except PaperlessException:
            msg = f' {plex_customer_id}, Invalid Sold To Address, street:{a_account.address1} city:{a_account.city} ' \
                  f'state:{a_account.state} zip:{a_account.postal_code} country:{a_account.country}'
            logger.debug(msg)
            logger.warning(f'Exception catch in AccountImportProcessor while attempting account update for '
                           f'sold to address for account: {plex_customer_id} ')

    @staticmethod
    def scrub_phone_number(phone_num: str):
        return re.sub('[^0-9]', '', phone_num)[0:10]

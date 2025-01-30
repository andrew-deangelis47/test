from plex_v2.configuration import PlexConfig
from plex_v2.objects.customer import Customer, CustomerContact, CustomerAddress
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from paperless.objects.customers import Account, Contact, Facility, BillingAddress, Address
from baseintegration.datamigration import logger
from typing import List
from baseintegration.utils.address import AddressUtils
from paperless.exceptions import PaperlessException


class AccountUtils:

    def __init__(self, config: PlexConfig):
        self.config: PlexConfig = config
        self.default_country = 'USA'

    def get_plex_customer_by_code(self, code: str) -> Customer:
        """
        raises Cancellation Integration Action if the Plex Customer Does not exist
        """
        existing_customers = Customer.find_customers(code=code)
        existing_customer: Customer = existing_customers[0] if len(existing_customers) > 0 else None
        if existing_customer is None:
            raise CancelledIntegrationActionException(f'Invalid Plex customer Code provided to importer: {code}')
        return existing_customer

    def get_existing_pp_account(self, code: str):
        accounts = Account.filter(code)
        if len(accounts) == 0:
            return None

        pp_account = Account.get(id=accounts[0].id)
        return pp_account

    def get_and_validate_contacts(self, erp_code) -> List[CustomerContact]:
        plex_customer_id = self._get_plex_customer_id(erp_code)
        plex_contacts = CustomerContact.find_customer_contacts(plex_customer_id)

        plex_contact: CustomerContact
        for plex_contact in plex_contacts:
            self._validate_contact_has_required_info(plex_contact, erp_code)

        return plex_contacts

    # def does_contact_exist_by_email(self):

    def get_contact_emails_for_account(self, pp_account: Account):
        emails = []
        pp_contacts = Contact.filter(account_id=pp_account.id)
        pp_contact: Contact
        for pp_contact in pp_contacts:
            emails.append(pp_contact.email)

        return emails

    def get_plex_addresses(self, plex_customer: Customer) -> tuple:
        """
        returns lists of billing, and ship to addresses, and one sold to address (the last one we get),
        """
        billing: List[CustomerAddress] = []
        facilities: List[CustomerAddress] = []
        sold_to: CustomerAddress = None

        plex_locations: [CustomerAddress] = CustomerAddress.find_customer_addresses(
            code=None,
            billTo=None,
            remitTo=None,
            shipTo=None,
            soldTo=None,
            resource_name_kwargs={
                'customer_id': plex_customer.id
            }
        )

        plex_location: CustomerAddress
        for plex_location in plex_locations:
            if plex_location.billTo:
                billing.append(plex_location)
            if plex_location.soldTo:
                sold_to = plex_location
            if plex_location.shipTo:
                facilities.append(plex_location)

        return (billing, facilities, sold_to)

    def _validate_contact_has_required_info(self, plex_contact: CustomerContact, erp_code: str) -> None:
        """
        validates email, first name, last name
        """
        if plex_contact.email is None or plex_contact.email.strip() == '':
            raise CancelledIntegrationActionException(f'A plex contact under account {erp_code} has an invalid email address. Please fix in order to import this account fully')
        if plex_contact.firstName is None or plex_contact.firstName.strip() == '':
            raise CancelledIntegrationActionException(f'A plex contact under account {erp_code} has an invalid first name. Please fix in order to import this account fully')
        if plex_contact.lastName is None or plex_contact.lastName.strip() == '':
            raise CancelledIntegrationActionException(f'A plex contact under account {erp_code} has an invalid last name. Please fix in order to import this account fully')

    def _get_plex_customer_id(self, erp_code) -> str:
        plex_customers = Customer.find_customers(code=erp_code)
        if len(plex_customers) == 0:
            raise CancelledIntegrationActionException(f'Invalid Plex customer Code provided to importer: {erp_code}')

        return plex_customers[0].id

    def create_address(self, plex_customer_id: str, pp_account: str, use_address_prefix: bool, use_addr_code_for_facility_name: bool):
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
        plex_location: CustomerAddress
        for plex_location in plex_locations:
            country_alpha_3, state_province_name = AddressUtils.get_country_and_state(plex_location.country.strip(),
                                                                                      plex_location.state.strip(),
                                                                                      plex_location.zip[0:5].strip(),
                                                                                      self.default_country)

            if plex_location.billTo:
                self.add_billing(plex_customer_id, pp_account.id, plex_location, pp_billings, state_province_name,
                                 country_alpha_3, use_address_prefix)

            if plex_location.shipTo:
                self.add_facility(plex_customer_id, pp_account.id, plex_location, pp_facilities, state_province_name,
                                  country_alpha_3, use_addr_code_for_facility_name)

    def add_facility(self, plex_customer_id: str, pp_account_id: str, plex_location: CustomerAddress,
                     pp_facilities: [Facility], state_province_name: str, country_alpha_3: str, use_address_code_for_facility_name: bool):
        create = False
        pp_address = None
        name = plex_location.name
        if use_address_code_for_facility_name:
            name = plex_location.code
        for pp_facility in pp_facilities:
            if pp_facility.name == name:
                pp_address = Facility.get(id=pp_facility.id)
                break
        if pp_address is None:
            create = True
            pp_address = Facility(account_id=pp_account_id, name=name, attention=" ")
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
            logger.warning(f'Exception catch in AccountImportProcessor while attempting to add '
                           f'Facility address: {plex_customer_id}-{plex_location.name}')
            raise CancelledIntegrationActionException(f_msg)

    def add_billing(self, plex_customer_id: str, pp_account_id: str, plex_location: CustomerAddress,
                    pp_billings: [BillingAddress], state_province_name: str, country_alpha_3: str, use_address_prefix: bool):
        for pp_billing in pp_billings:
            if pp_billing.address1 == plex_location.address.strip() and \
                    pp_billing.city == plex_location.city.strip() and \
                    pp_billing.country == country_alpha_3 and pp_billing.state == state_province_name and \
                    pp_billing.postal_code == plex_location.zip[0:5].strip():
                return
        address = plex_location.address.strip()
        if use_address_prefix:
            address = plex_location.code + '-' + address
        pp_address = BillingAddress(address1=address, city=plex_location.city.strip(),
                                    state=state_province_name, postal_code=plex_location.zip[0:5].strip(),
                                    country=country_alpha_3)
        try:
            pp_address.create(account_id=pp_account_id)
        except PaperlessException:
            b_msg = f' {plex_customer_id}, Invalid Billing Address, street:{pp_address.address1} ' \
                    f'city:{pp_address.city} state:{pp_address.state} zip:{pp_address.postal_code} ' \
                    f'country:{pp_address.country}'
            logger.warning(f'Exception catch in AccountImportProcessor while attempting to add '
                           f'Billing address: {plex_customer_id}-Billing-{plex_location.name}')
            raise CancelledIntegrationActionException(b_msg)

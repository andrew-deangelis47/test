from paperless.objects.customers import Account
from sage.models.sage_models.customer import Customer, Address
from paperless.objects.customers import Address as PaperlessAddress, Contact as PaperlessContact
from sage.models.sage_models.customer import Contact
from baseintegration.exporter import logger
import pycountry
from typing import Union

CUST_DEFAULT_ADDR_CODE = 'DEFAULT'
CUST_BILLING_ADDR_CODE = 'BILL'
CUST_SHIP_ADDR_CODE = 'SHIP'

DEFAULT_CURRENCY = 'USD'
DEFAULT_TAX_RULE = 'OOS'
DEFAULT_ACCOUNTING_CODE = 'STD'
DEFAULT_PAYMENT_DAYS = 'USPREPAY'
DEFAULT_CATEGORY = 'US'


def get_country_code_from_account(account: Account) -> str:
    """
    If it's any other country besides USA, set to EXP
    """
    if account.sold_to_address.country == 'USA':
        return 'US'
    return 'EXP'


def convert_country_code(country_code: str) -> Union[str, bool]:
    """
    converts 3 character country code to 2
    """
    for country in pycountry.countries:
        if country.alpha_3 == country_code:
            return country.alpha_2
    return False


def get_customer_from_account(paperless_account: Account) -> Customer:

    # assign the basic stuff
    cust = Customer()
    # logger.info(cust.company_name)
    # logger.info(cust.default_address)
    # logger.info(cust.bill_to_customer_address)
    cust.company_name = paperless_account.name

    # address codes
    cust.default_address = CUST_DEFAULT_ADDR_CODE
    cust.bill_to_customer_address = CUST_BILLING_ADDR_CODE
    cust.default_ship_to_address = CUST_SHIP_ADDR_CODE

    # currently there is no mappings for these, but they are required to create a sage customer
    # we'll use these defaults for now
    cust.currency = DEFAULT_CURRENCY
    cust.tax_rule = DEFAULT_TAX_RULE
    cust.accounting_code = DEFAULT_ACCOUNTING_CODE
    cust.payment_days = DEFAULT_PAYMENT_DAYS
    cust.category = get_country_code_from_account(paperless_account)

    return cust


def _paperless_address_to_sage_address(paperless_address: PaperlessAddress, code: str,
                                       paperless_account_website: str) -> Address:
    sage_address = Address()
    sage_address.address_id = code
    sage_address.address_line_1 = paperless_address.address1
    sage_address.address_line_2 = paperless_address.address2
    sage_address.city = paperless_address.city
    sage_address.state = paperless_address.state
    sage_address.website = paperless_account_website

    # convert 3 digit country code to 2, and set
    country_code = convert_country_code(paperless_address.country)
    if country_code:
        sage_address.country = country_code
    else:
        logger.info('cannot convert country code from alpha3 to alpha2: ' + country_code)
        sage_address.country = ''
    sage_address.zip_code = paperless_address.postal_code

    # we dont have the concept of address telephone in paperless, set to blank?
    sage_address.telephone = ''

    # we dont have the concept of description in paperless, set to blank?
    sage_address.description = ''

    return sage_address


def get_customer_contacts(paperless_account: Account) -> list:
    paperless_contacts = PaperlessContact.filter(account_id=paperless_account.id)
    sage_contacts = []
    for paperless_contact in paperless_contacts:
        sage_contacts.append(_get_sage_contact_from_paperless_contact(paperless_contact))

    return sage_contacts


def _get_sage_contact_from_paperless_contact(paperless_contact: PaperlessContact) -> Contact:
    sage_contact = Contact()
    sage_contact.email = paperless_contact.email
    sage_contact.first_name = paperless_contact.first_name
    sage_contact.last_name = paperless_contact.last_name

    return sage_contact


def get_customer_billing_addresses(paperless_account: Account, address_code: str) -> Address:
    paperless_billing_addresses = paperless_account.billing_addresses
    sage_addresses = []
    for paperless_billing_address in paperless_billing_addresses:
        sage_addresses.append(
            _paperless_address_to_sage_address(paperless_billing_address, address_code, paperless_account.url))

    return sage_addresses


def populate_addresses_from_paperless_account(paperless_account: Account) -> Customer:
    cust_sold_to_address = get_customer_default_address(paperless_account, CUST_DEFAULT_ADDR_CODE)
    cust_default_address = get_customer_default_address(paperless_account, CUST_SHIP_ADDR_CODE)
    cust_bill_addresses = get_customer_billing_addresses(paperless_account, CUST_BILLING_ADDR_CODE)
    cust_bill_address = None
    if len(cust_bill_addresses) > 0:
        cust_bill_address = cust_bill_addresses[0]

    return [cust_bill_address, cust_sold_to_address, cust_default_address]


def get_customer_default_address(paperless_account: Account, address_code: str) -> Address:
    paperless_address = paperless_account.sold_to_address
    if paperless_address is None:
        return None
    return _paperless_address_to_sage_address(paperless_address, address_code, paperless_account.url)


class PaperlessAccountToSageCustomerIFileConverter:

    @staticmethod
    def to_sage_customer_i_file(paperless_account: Account) -> str:
        # customer
        sage_customer = get_customer_from_account(paperless_account)
        sage_customer_i_file = sage_customer.to_i_file()

        # addresses
        addresses_i_file = ''
        sage_addresses = populate_addresses_from_paperless_account(paperless_account)
        for sage_address in sage_addresses:
            if sage_address is not None:
                addresses_i_file += sage_address.to_i_file()

        # contacts
        contacts_i_file = ''
        sage_contacts = get_customer_contacts(paperless_account)
        for sage_contact in sage_contacts:
            contacts_i_file += sage_contact.to_i_file()

        return sage_customer_i_file + addresses_i_file + contacts_i_file + 'END'

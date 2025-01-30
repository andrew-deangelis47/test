from sage.models.sage_models.customer.customer import Customer as SageCustomer
from sage.models.sage_models.customer.address import Address as SageAddress
from paperless.objects.customers import Account
from sage.models.converters.sage_address_to_paperless_address_converter import SageAddressToPaperlessAddressConverter
from sage.models.converters.sage_address_to_paperless_billing_address_converter import SageAddressToPaperlessBillingAddressConverter
from baseintegration.datamigration import logger


def _is_blank(some_str: str) -> bool:
    return len(some_str.strip()) == 0


def _validate_sage_address(sage_address: SageAddress) -> bool:
    # Assign address attributes
    address_fields = (
        sage_address.address_line_1,
        sage_address.city,
        sage_address.state,
        sage_address.zip_code
    )

    # Check if address has enough criteria for Paperless Parts address validation
    not_none = all([field is not None for field in address_fields])
    not_blank = all([not _is_blank(field) for field in address_fields])
    return not_blank and not_none


def get_sage_address_by_key(key: str, sage_addresses: list) -> SageAddress:
    for sage_address in sage_addresses:
        if sage_address.address_id == key:
            return sage_address
    return None


class SageCustomerToPaperlessAccountConverter:

    @staticmethod
    def to_paperless_account(sage_customer: SageCustomer, sage_addresses: list) -> Account:
        # 1) instantiate account with min required properties
        paperless_account = Account(
            name=sage_customer.company_name,
            erp_code=sage_customer.code
        )

        # 2) validate and set sold to address for account
        #    sage default address -> paperless account sold to address
        sage_default_address = get_sage_address_by_key(sage_customer.default_address, sage_addresses)
        if _validate_sage_address(sage_default_address):
            paperless_account.sold_to_address = SageAddressToPaperlessAddressConverter.to_paperless_address(
                sage_default_address,
                sage_customer.code
            )
        else:
            logger.error('Sage customer default address is not a valid address')
            logger.error('Not setting sold to address for account for customer ' + sage_customer.code)

        # 3) validate and set billing address for account
        # sage bill to customer address -> paperless account billing address
        sage_billing_address = get_sage_address_by_key(sage_customer.bill_to_customer_address, sage_addresses)
        if _validate_sage_address(sage_billing_address):
            paperless_account.billing_addresses = [
                SageAddressToPaperlessBillingAddressConverter.to_paperless_billing_address(
                    sage_billing_address,
                    sage_customer.code
                )]
        else:
            logger.error('Sage customer default billing address is not a valid address')
            logger.error('Not setting billing address for account for customer ' + sage_customer.code)

        # 4) set the other cool stuff
        paperless_account.phone = sage_default_address.telephone[0:10]
        paperless_account.url = sage_default_address.website

        return paperless_account

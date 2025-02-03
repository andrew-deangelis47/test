import unittest
from sage.models.sage_models.customer.customer import Customer as SageCustomer
from sage.models.sage_models.customer.address import Address as SageAddress
from sage.models.converters.sage_customer_to_paperless_account_converter import SageCustomerToPaperlessAccountConverter


class TestSageCustomerToPaperlessAccountConverter(unittest.TestCase):
    # test constants
    sage_customer = None
    paperless_account = None

    def setUp(self) -> None:
        # construct sage customer's billing address
        bill_to_customer_address = SageAddress()
        bill_to_customer_address.address_id = 'BILL'
        bill_to_customer_address.address_line_1 = 'address_line_1'
        bill_to_customer_address.address_line_2 = 'address_line_2'
        bill_to_customer_address.city = 'city'
        bill_to_customer_address.state = 'state'
        bill_to_customer_address.country = 'country'
        bill_to_customer_address.zip_code = 'zip'
        bill_to_customer_address.phone_numbers = 'phone'
        bill_to_customer_address.website = 'website'

        default_address = SageAddress()
        default_address.address_id = 'MAIN'
        default_address.address_line_1 = 'address_line_1'
        default_address.address_line_2 = 'address_line_2'
        default_address.city = 'city'
        default_address.state = 'state'
        default_address.country = 'country'
        default_address.zip_code = 'zip'
        default_address.telephone = 'phone'
        default_address.website = 'website'

        # construct sage customer
        self.sage_customer = SageCustomer
        self.sage_customer.code = 'code'
        self.sage_customer.company_name = 'company_name'
        self.sage_customer.bill_to_customer_address = 'BILL'
        self.sage_customer.default_address = 'MAIN'

        # use converter to get paperless account
        self.paperless_account = \
            SageCustomerToPaperlessAccountConverter.to_paperless_account(
                self.sage_customer, [bill_to_customer_address, default_address])

    def test_to_paperless_account_sets_erp_code_to_sage_customer_code(self):
        self.assertEqual(self.paperless_account.erp_code, self.sage_customer.code)

    def test_to_paperless_account_sets_account_name_to_sage_customer_company_name(self):
        self.assertEqual(self.paperless_account.name, self.sage_customer.company_name)

    def test_to_paperless_account_sets_billing_addresses_to_sage_customer_bill_to_customer_address(self):
        # TODO: we need to test this in a different way - we are mapping the list of addresses to the sold to address key
        # self.assertIs(self.paperless_account.billing_addresses[0], paperless.objects.customers.BillingAddress)
        assert 1

    def test_to_paperless_account_sets_sold_to_address_to_sage_customer_default_address(self):
        # TODO: we need to test this in a different way - we are mapping the list of addresses to the sold to address key
        # self.assertIs(self.paperless_account.sold_to_address, paperless.objects.customers.Address)
        assert 1

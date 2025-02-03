import paperless.objects.customers
from sage.models.sage_models.customer.customer import Customer as SageCustomer
from sage.models.sage_models.customer.address import Address as SageAddress
from sage.models.sage_models.customer.contact import Contact as SageContact
from sage.models.sage_models.customer.customer_full_entity import SageCustomerFullEntity
from sage.models.converters.sage_customer_to_paperless_facility_converter import SageCustomerToPaperlessFacilityConverter
import unittest


class TestSageCustomerToPaperlessFacility(unittest.TestCase):
    ACCOUNT_ID = 1234
    sage_customer = None
    paperless_facility = None

    def setUp(self) -> None:
        ship_to_address = SageAddress
        ship_to_address.address_id = 'SHIP'
        ship_to_address.address_line_1 = 'address_line_1'
        ship_to_address.address_line_2 = 'address_line_2'
        ship_to_address.city = 'city'
        ship_to_address.state = 'state'
        ship_to_address.country = 'country'
        ship_to_address.zip_code = 'zip'
        ship_to_address.phone_numbers = 'phone'
        ship_to_address.website = 'website'

        sage_customer = SageCustomer
        sage_customer.default_ship_to_address = 'SHIP'
        sage_customer.code = 'code'
        sage_customer.company_name = 'company_name'

        sage_contact = SageContact
        sage_contact.first_name = 'contact_first_name'
        sage_contact.last_name = 'contact_last_name'
        sage_contact.email = 'contact_email'

        sage_full_cust = SageCustomerFullEntity
        sage_full_cust.customer = sage_customer
        sage_full_cust.addresses = [ship_to_address]
        sage_full_cust.contacts = [sage_contact]

        self.sage_customer = sage_customer
        self.paperless_facility = SageCustomerToPaperlessFacilityConverter.to_paperless_facility(sage_full_cust, self.ACCOUNT_ID)

    def test_to_paperless_facility_sets_account_id_to_paperless_facility_account_id(self):
        self.assertEqual(self.paperless_facility.account_id, self.ACCOUNT_ID)

    def test_to_paperless_facility_sets_sage_ship_to_address_to_paperless_facility_address(self):
        # asserting that this address property is set as a paperless address
        # the test for the address conversion is in TestSageAddressToPaperlessBillingAddressConverter
        self.assertIs(self.paperless_facility.address, paperless.objects.customers.Address)

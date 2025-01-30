from plex_v2.factories.plex.customer_address import PlexCustomerAddressFactory
from plex_v2.configuration import PlexConfig
from unittest.mock import create_autospec
from plex_v2.utils.export import ExportUtils
from plex_v2.objects.customer import Customer
from paperless.objects.address import AddressInfo


class TestPlexCustomerAddressFactory:

    VALID_PLEX_CUSTOMER_ID = 'VALID_PLEX_CUSTOMER_ID'
    VALID_FACILITY_NAME = 'VALID_FACILITY_NAME'
    VALID_ADDR_1 = 'VALID_ADDR_1'
    VALID_ADDR_2 = 'VALID_ADDR_2'
    VALID_CITY = 'VALID_CITY'
    VALID_STATE = 'VALID_STATE'
    VALID_POSTAL_CODE = 'VALID_POSTAL_CODE'
    VALID_COUNTRY = 'VALID_COUNTRY'
    VALID_PHONE = 'VALID_PHONE'
    VALID_ALT_CODE = 'VALID_ALT_CODE'

    def setup_method(self):
        self.config = create_autospec(PlexConfig)

        self.utils = create_autospec(ExportUtils)

        self.factory = PlexCustomerAddressFactory(
            config=self.config,
            utils=self.utils
        )

        self.customer = create_autospec(Customer)
        self.customer.id = self.VALID_PLEX_CUSTOMER_ID

        self.address_info = create_autospec(AddressInfo)
        self.address_info.facility_name = self.VALID_FACILITY_NAME
        self.address_info.address1 = self.VALID_ADDR_1
        self.address_info.address2 = self.VALID_ADDR_2
        self.address_info.city = self.VALID_CITY
        self.address_info.state = self.VALID_STATE
        self.address_info.postal_code = self.VALID_POSTAL_CODE
        self.address_info.country = self.VALID_COUNTRY
        self.address_info.phone = self.VALID_PHONE

        self.alt_code = self.VALID_ALT_CODE

    def test_to_plex_customer_address_sets_address_to_account_addr1_plus_addr2(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert plex_customer.address == f'{self.address_info.address1} {self.address_info.address2}'

    def test_to_plex_customer_address_sets_city_to_account_city(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert plex_customer.city == self.address_info.city

    def test_to_plex_customer_address_sets_state_to_account_state(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert plex_customer.state == self.address_info.state

    def test_to_plex_customer_address_sets_zip_to_account_postal_code(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert plex_customer.zip == self.address_info.postal_code

    def test_to_plex_customer_address_sets_country_to_account_country(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert plex_customer.country == self.address_info.country

    def test_to_plex_customer_address_sets_customer_id_to_associated_plex_customers_id(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert plex_customer.customerId == self.customer.id

    def test_to_plex_customer_address_sets_active_to_true(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert plex_customer.active

    def test_to_plex_customer_address_sets_code_to_alt_code_passed_in(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert plex_customer.code == self.alt_code

    def test_to_plex_customer_address_sets_phone_to_accounts_phone(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert plex_customer.phone == self.address_info.phone

    def test_to_plex_customer_address_sets_billTo_to_false_if_shipping_address(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert not plex_customer.billTo

    def test_to_plex_customer_address_sets_billTo_to_true_if_not_shipping_address(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            False,
            self.alt_code
        )

        assert plex_customer.billTo

    def test_to_plex_customer_address_sets_shipTo_to_true_if_shipping_address(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert plex_customer.shipTo

    def test_to_plex_customer_address_sets_shipTo_to_false_if_not_shipping_address(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            False,
            self.alt_code
        )

        assert not plex_customer.shipTo

    def test_to_plex_customer_address_sets_remitTo_to_false_if_shipping_address(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert not plex_customer.remitTo

    def test_to_plex_customer_address_sets_remitTo_to_true_if_not_shipping_address(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            False,
            self.alt_code
        )

        assert plex_customer.remitTo

    def test_to_plex_customer_address_sets_soldTo_to_true_if_not_shipping_address(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            False,
            self.alt_code
        )

        assert plex_customer.soldTo

    def test_to_plex_customer_address_sets_soldTo_to_false_if_shipping_address(self):
        plex_customer = self.factory.to_plex_customer_address(
            self.customer,
            self.address_info,
            True,
            self.alt_code
        )

        assert not plex_customer.soldTo

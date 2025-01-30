from plex.objects.customer import Customer
from plex.exporter.processors.customer import CustomerProcessor
from plex.configuration import PlexConfig
from paperless.objects.address import AddressInfo
from faker import Faker
from unittest.mock import patch
from types import SimpleNamespace


class TestCustomerProcessor:
    def setup(self) -> None:
        self.processor = CustomerProcessor(SimpleNamespace(
            erp_config=PlexConfig(
                default_part_type='part_type',
                default_part_group='part_group',
                default_part_status='part_status',
                default_product_type='product_type',
            )
        ))
        fake = Faker()
        self.address_info = AddressInfo(
            attention=fake.name(),
            address1=fake.street_address(),
            city=fake.city(),
            postal_code=fake.postcode(),
            country=fake.country_code(representation='alpha-3'),
            phone="1234",
            phone_ext="100",
            business_name=fake.name(),
            facility_name="test",
            state="ME"
        )

    def test_new_customer_with_erpcode(self, caplog):
        order_account = SimpleNamespace(
            name='Test Company',
            erp_code='CODE',
            notes='test',
        )
        with patch.object(Customer, 'find_customers', return_value=[]), \
                patch.object(Customer, 'create', return_value=None):
            self.processor._process(
                order_account,
                billing_info=self.address_info,
                shipping_info=self.address_info
            )
            assert "Creating new customer with code CODE and name Test Company" in caplog.text

    def test_new_customer_without_erpcode(self, caplog):
        self.setup()
        order_account = SimpleNamespace(
            name='Test Company',
            erp_code=None,
            notes=None,
        )
        with patch.object(Customer, 'find_customers', return_value=[]), \
                patch.object(Customer, 'create', return_value=None):
            self.processor._process(
                order_account,
                billing_info=self.address_info,
                shipping_info=self.address_info
            )
            assert "Creating new customer with code None and name Test Company" in caplog.text

    def test_existing_customer_with_erpcode(self, caplog):
        order_account = SimpleNamespace(
            name='Test Company',
            erp_code='CODE',
            notes='test',
        )
        with patch.object(Customer, 'find_customers', return_value=[Customer(name="Test Company", code="CODE", status="Active", type="type")]), \
                patch.object(Customer, 'create', return_value=None):
            self.processor._process(
                order_account,
                billing_info=self.address_info,
                shipping_info=self.address_info
            )
            assert "Existing customer (code: CODE) found, using this one" in caplog.text

    def test_new_customer_create_disabled(self, caplog):
        self.setup()
        order_account = SimpleNamespace(
            name='Test Company',
            erp_code=None,
            notes=None,
        )
        with patch.object(Customer, 'find_customers', return_value=[]), \
                patch.object(Customer, 'create', return_value=None):
            processed_customer = self.processor._process(
                order_account,
                billing_info=self.address_info,
                shipping_info=self.address_info,
                create=False
            )
            assert processed_customer is None
            assert "Customer creation disabled" in caplog.text

from plex_v2.factories.plex.customer_contact import PlexCustomerContactFactory
from plex_v2.configuration import PlexConfig
from unittest.mock import create_autospec
from plex_v2.utils.export import ExportUtils
from paperless.objects.orders import OrderContact
from plex_v2.objects.customer import Customer


class TestCustomerContactFactory:

    VALID_EMAIL = 'VALID_EMAIL'
    VALID_FIRST_NAME = 'VALID_FIRST_NAME'
    VALID_LAST_NAME = 'VALID_LAST_NAME'
    VALID_PHONE = 'VALID_PHONE'
    VALID_NOTES = 'VALID_NOTES'
    VALID_CUST_ID = 'VALID_CUST_ID'

    def setup_method(self):
        self.config = create_autospec(PlexConfig)

        self.utils = create_autospec(ExportUtils)

        self.factory = PlexCustomerContactFactory(
            config=self.config,
            utils=self.utils
        )

        self.contact = create_autospec(OrderContact)
        self.contact.email = self.VALID_EMAIL
        self.contact.first_name = self.VALID_FIRST_NAME
        self.contact.last_name = self.VALID_LAST_NAME
        self.contact.phone = self.VALID_PHONE
        self.contact.notes = self.VALID_NOTES

        self.customer = create_autospec(Customer)
        self.customer.id = self.VALID_CUST_ID

        self.last_sort_order = 1

    def test_to_customer_contact_sets_customerId_to_associated_customers_id(self):
        customer_contact = self.factory.to_customer_contact(
            self.contact,
            self.customer,
            self.last_sort_order
        )

        assert customer_contact.customerId == self.customer.id

    def test_to_customer_contact_sets_email_to_contact_email(self):
        customer_contact = self.factory.to_customer_contact(
            self.contact,
            self.customer,
            self.last_sort_order
        )

        assert customer_contact.email == self.contact.email

    def test_to_customer_contact_sets_first_name_to_contact_first_name(self):
        customer_contact = self.factory.to_customer_contact(
            self.contact,
            self.customer,
            self.last_sort_order
        )

        assert customer_contact.firstName == self.contact.first_name

    def test_to_customer_contact_sets_last_name_to_contact_last_name(self):
        customer_contact = self.factory.to_customer_contact(
            self.contact,
            self.customer,
            self.last_sort_order
        )

        assert customer_contact.lastName == self.contact.last_name

    def test_to_customer_contact_sets_phone_to_contact_phone(self):
        customer_contact = self.factory.to_customer_contact(
            self.contact,
            self.customer,
            self.last_sort_order
        )

        assert customer_contact.phone == self.contact.phone

    def test_to_customer_contact_sets_note_to_contact_notes(self):
        customer_contact = self.factory.to_customer_contact(
            self.contact,
            self.customer,
            self.last_sort_order
        )

        assert customer_contact.note == self.contact.notes

    def test_to_customer_contact_sets_sort_order_to_one_more_than_previous_sort_order(self):
        customer_contact = self.factory.to_customer_contact(
            self.contact,
            self.customer,
            self.last_sort_order
        )

        assert customer_contact.sortOrder == self.last_sort_order + 1

    def test_to_customer_contact_sets_private_to_zero(self):
        customer_contact = self.factory.to_customer_contact(
            self.contact,
            self.customer,
            self.last_sort_order
        )

        assert customer_contact.private == 0

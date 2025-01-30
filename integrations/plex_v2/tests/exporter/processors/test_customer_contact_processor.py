from plex_v2.exporter.processors.customer_contact import ContactProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from baseintegration.integration.integration_export_report import IntegrationExportReport
from paperless.objects.orders import Order, OrderContact
from plex_v2.objects.customer import Customer, CustomerContact
from plex_v2.factories.plex.customer_contact import PlexCustomerContactFactory
from plex_v2.utils.export import ExportUtils


class TestApprovedShipToProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = ContactProcessor(SimpleNamespace(
            erp_config=PlexConfig(
                can_creat_new_customers=True
            ),
            integration_report=integration_report
        ))

        self.order = create_autospec(Order)
        self.order.contact = create_autospec(OrderContact)
        self.customer = create_autospec(Customer)
        self.factory = create_autospec(PlexCustomerContactFactory)
        self.utils = create_autospec(ExportUtils)

    def test_customer_contact_processor_returns_existing_contact_if_one_exists(self):
        existing_contact = create_autospec(CustomerContact)
        existing_contact.email = 'email'
        existing_contact.firstName = 'firstName'
        existing_contact.lastName = 'lastName'

        self.utils.get_existing_plex_contact_and_sort_order.return_value = existing_contact, 0

        contact = self.processor._process(
            self.order,
            self.customer,
            self.factory,
            self.utils
        )

        assert contact.email == existing_contact.email
        assert contact.firstName == existing_contact.firstName
        assert contact.lastName == existing_contact.lastName

    def test_customer_contact_processor_creates_new_customer_if_one_not_exists(self):
        created_contact = create_autospec(CustomerContact)
        created_contact.email = 'email'
        created_contact.firstName = 'firstName'
        created_contact.lastName = 'lastName'

        self.factory.to_customer_contact.return_value = created_contact
        self.utils.get_existing_plex_contact_and_sort_order.return_value = None, 0

        self.processor._process(
            self.order,
            self.customer,
            self.factory,
            self.utils
        )

        self.factory.to_customer_contact.assert_called_once()
        created_contact.create.assert_called_once()

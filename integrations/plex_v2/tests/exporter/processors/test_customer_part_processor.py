from plex_v2.exporter.processors.customer_part import CustomerPartProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from baseintegration.integration.integration_export_report import IntegrationExportReport
from paperless.objects.orders import OrderItem, OrderComponent
from plex_v2.utils.export import ExportUtils
from plex_v2.factories.plex.customer_part import CustomerPartFactory
from plex_v2.objects.customer import Customer, CustomerPart
from plex_v2.objects.part import Part


class TestCustomerPartProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = CustomerPartProcessor(SimpleNamespace(
            erp_config=PlexConfig(),
            integration_report=integration_report
        ))

        self.plex_part = create_autospec(Part)
        self.plex_part.number = 'number'

        self.utils = create_autospec(ExportUtils)
        self.utils.get_top_level_part_from_order_item.return_value = None
        self.utils.get_plex_part_from_paperless_component.return_value = None

        self.order_component = create_autospec(OrderComponent)
        self.order_component.part_number = '1'

        self.customer_part = create_autospec(CustomerPart)
        self.customer_part.number = 'number'

        self.customer_part_factory = create_autospec(CustomerPartFactory)
        self.customer_part_factory.to_customer_part.return_value = self.customer_part

        self.order_item = create_autospec(OrderItem)

        self.customer = create_autospec(Customer)
        self.customer.name = 'name'

    def test_customer_part_processor_creates_customer_part_if_not_exists(self):
        self.utils.get_customer_part_if_exists.return_value = None

        self.processor._process(
            self.order_item,
            self.customer,
            self.utils,
            self.customer_part_factory
        )

        self.customer_part.create.assert_called_once()

    def test_routing_processor_does_not_create_routing_if_ignored_operation(self):
        self.utils.get_plex_part_from_paperless_component.return_value = self.plex_part
        self.utils.get_customer_part_if_exists.return_value = self.customer_part

        self.processor._process(
            self.order_item,
            self.customer,
            self.utils,
            self.customer_part_factory
        )

        self.customer_part.create.assert_not_called()

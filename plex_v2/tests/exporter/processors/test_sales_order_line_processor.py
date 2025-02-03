from plex_v2.exporter.processors.sales_order_line import SalesOrderLineProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from baseintegration.integration.integration_export_report import IntegrationExportReport
from plex_v2.objects.sales_orders import SalesOrderLine, SalesOrder
from plex_v2.factories.plex.sales_order_line import SalesOrderLineFactory
from plex_v2.factories.plex.sales_order_line_price import SalesOrderLinePriceFactory
from plex_v2.objects.plex_part_to_plex_customer_part_mapping import PlexPartToPlexCustomerPartMapping
from plex_v2.objects.customer import CustomerPart
from paperless.objects.orders import OrderItem
from plex_v2.objects.part import Part


class TestApprovedShipToProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = SalesOrderLineProcessor(SimpleNamespace(
            erp_config=PlexConfig(),
            integration_report=integration_report
        ))

        self.customer_part = create_autospec(CustomerPart)
        self.plex_part = create_autospec(Part)
        self.order_item = create_autospec(OrderItem)
        self.mapping = create_autospec(PlexPartToPlexCustomerPartMapping)
        self.mapping.customer_part = self.customer_part
        self.mapping.part = self.plex_part
        self.mapping.pp_order_item = self.order_item
        self.sales_order = create_autospec(SalesOrder)
        self.sales_order.poNumber = 'poNumber'
        self.ship_to_addr = 'ship_to_addr'
        self.line_no = 1
        self.factory = create_autospec(SalesOrderLineFactory)
        self.line_price_factory = create_autospec(SalesOrderLinePriceFactory)

    def test_sales_order_line_processor_creates_sales_order_line_model(self):
        self.processor._process(
            self.mapping,
            self.sales_order,
            self.line_no,
            self.factory,
            self.line_price_factory
        )

        self.factory.to_sales_order_line.assert_called_once()

    def test_sales_order_line_processor_creates_sales_order_line_price_model(self):
        self.processor._process(
            self.mapping,
            self.sales_order,
            self.line_no,
            self.factory,
            self.line_price_factory
        )

        self.line_price_factory.to_sales_order_line_price.assert_called_once()

    def test_sales_order_line_processor_adds_line_price_to_order_line(self):
        sales_order_line = create_autospec(SalesOrderLine)
        self.factory.to_sales_order_line.return_value = sales_order_line

        self.processor._process(
            self.mapping,
            self.sales_order,
            self.line_no,
            self.factory,
            self.line_price_factory
        )

        sales_order_line.add_line_price.assert_called_once()

    def test_sales_order_line_processor_creates_sales_order_line(self):
        sales_order_line = create_autospec(SalesOrderLine)
        self.factory.to_sales_order_line.return_value = sales_order_line

        self.processor._process(
            self.mapping,
            self.sales_order,
            self.line_no,
            self.factory,
            self.line_price_factory
        )

        sales_order_line.create.assert_called_once()

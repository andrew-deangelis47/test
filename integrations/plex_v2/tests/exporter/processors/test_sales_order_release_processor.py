from plex_v2.exporter.processors.sales_order_release import SalesOrderReleaseProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from baseintegration.integration.integration_export_report import IntegrationExportReport
from plex_v2.objects.sales_orders import SalesOrderLine
from plex_v2.objects.sales_orders import SalesOrderRelease
from plex_v2.factories.plex.sales_order_release import SalesOrderReleaseFactory
from paperless.objects.orders import OrderItem


class TestApprovedShipToProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = SalesOrderReleaseProcessor(SimpleNamespace(
            erp_config=PlexConfig(),
            integration_report=integration_report
        ))

        self.order_item = create_autospec(OrderItem)
        self.ship_to_addr_id = 'ship_to_addr_id'
        self.sales_order_line = create_autospec(SalesOrderLine)
        self.factory = create_autospec(SalesOrderReleaseFactory)

    def test_sales_order_release_processor_calls_factory_to_create_release_model(self):
        self.processor._process(
            self.order_item,
            self.ship_to_addr_id,
            self.sales_order_line,
            self.factory
        )

        self.factory.to_sales_order_release.assert_called_once()

    def test_sales_order_release_processor_creates_sales_order_release(self):
        sales_order_release = create_autospec(SalesOrderRelease)
        self.factory.to_sales_order_release.return_value = sales_order_release

        self.processor._process(
            self.order_item,
            self.ship_to_addr_id,
            self.sales_order_line,
            self.factory
        )

        sales_order_release.create.assert_called_once()

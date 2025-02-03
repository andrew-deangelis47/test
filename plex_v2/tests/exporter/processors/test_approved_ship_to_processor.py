from plex_v2.exporter.processors.approved_ship_to import ApprovedShipToProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from baseintegration.integration.integration_export_report import IntegrationExportReport
from plex_v2.objects.sales_orders import SalesOrderLine
from plex_v2.factories.plex.approved_ship_to import ApprovedShipToFactory
from plex_v2.objects.sales_orders import SalesOrderLineApprovedShipTo


class TestApprovedShipToProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = ApprovedShipToProcessor(SimpleNamespace(
            erp_config=PlexConfig(),
            integration_report=integration_report
        ))

        self.approved_ship_to = create_autospec(SalesOrderLineApprovedShipTo)
        self.ship_to_addr_id = '1234'
        self.order_line = create_autospec(SalesOrderLine)
        self.factory = create_autospec(ApprovedShipToFactory)
        self.factory.to_approved_ship_to.return_value = self.approved_ship_to

    def test_approved_ship_to_processor_creates_approved_ship_to(self):
        self.processor._process(
            self.ship_to_addr_id,
            self.order_line,
            self.factory,
        )

        self.approved_ship_to.create.assert_called_once()

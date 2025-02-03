from plex_v2.exporter.processors.sales_order import SalesOrderProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from baseintegration.integration.integration_export_report import IntegrationExportReport
from paperless.objects.orders import Order
from plex_v2.objects.sales_orders import SalesOrder
from plex_v2.objects.customer import Customer
from plex_v2.utils.export import ExportUtils
from plex_v2.factories.plex.sales_order import SalesOrderFactory


class TestSalesOrderProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = SalesOrderProcessor(SimpleNamespace(
            erp_config=PlexConfig(),
            integration_report=integration_report
        ))

        self.order = create_autospec(Order)
        self.customer = create_autospec(Customer)
        self.tier = '3'
        self.po_number = '123'
        self.quote_num_w_rev = '5-4'
        self.bill_to_addr_id = 'bill_to_addr_id'
        self.ship_to_addr_id = 'ship_to_addr_id'
        self.utils = create_autospec(ExportUtils)
        self.factory = create_autospec(SalesOrderFactory)

    def test_sales_order_processor_uses_existing_sales_order_if_tier_3_and_existing_order(self):
        sales_order = create_autospec(SalesOrder)
        sales_order.customerId = '1234'
        sales_order.poNumber = '678987'
        self.utils.get_existing_sales_order_by_po_number_and_customer.return_value = sales_order
        self.tier = 3

        returned_sales_order = self.processor._process(
            self.order,
            self.customer,
            self.tier,
            self.po_number,
            self.quote_num_w_rev,
            self.bill_to_addr_id,
            self.ship_to_addr_id,
            self.utils,
            self.factory
        )

        assert sales_order.customerId == returned_sales_order.customerId
        assert sales_order.poNumber == returned_sales_order.poNumber

    def test_sales_order_processor_creates_sales_order_if_sales_order_exists_and_tier_is_2(self):
        sales_order = create_autospec(SalesOrder)
        sales_order.poNumber = '123'
        self.factory.to_tier_2_sales_order.return_value = sales_order
        self.utils.get_existing_sales_order_by_po_number_and_customer.return_value = sales_order
        self.utils.create_sales_order_if_not_already_exists.return_value = sales_order
        self.tier = 2

        self.processor._process(
            self.order,
            self.customer,
            self.tier,
            self.po_number,
            self.quote_num_w_rev,
            self.bill_to_addr_id,
            self.ship_to_addr_id,
            self.utils,
            self.factory
        )

        self.factory.to_tier_2_sales_order.assert_called_once()
        self.utils.create_sales_order_if_not_already_exists.assert_called_once()

    def test_sales_order_processor_creates_sales_order_if_sales_order_does_not_exist_and_tier_3(self):
        sales_order = create_autospec(SalesOrder)
        sales_order.poNumber = '123'
        self.factory.to_tier_3_sales_order.return_value = sales_order
        self.utils.get_existing_sales_order_by_po_number_and_customer.return_value = None
        self.utils.create_sales_order_if_not_already_exists.return_value = sales_order
        self.tier = 3

        self.processor._process(
            self.order,
            self.customer,
            self.tier,
            self.po_number,
            self.quote_num_w_rev,
            self.bill_to_addr_id,
            self.ship_to_addr_id,
            self.utils,
            self.factory
        )

        self.factory.to_tier_3_sales_order.assert_called_once()
        self.utils.create_sales_order_if_not_already_exists.assert_called_once()

    def test_sales_order_processor_creates_sales_order_if_sales_order_does_not_exist_and_tier_2(self):
        sales_order = create_autospec(SalesOrder)
        sales_order.poNumber = '123'
        self.factory.to_tier_2_sales_order.return_value = sales_order
        self.utils.get_existing_sales_order_by_po_number_and_customer.return_value = None
        self.utils.create_sales_order_if_not_already_exists.return_value = sales_order
        self.tier = 2

        self.processor._process(
            self.order,
            self.customer,
            self.tier,
            self.po_number,
            self.quote_num_w_rev,
            self.bill_to_addr_id,
            self.ship_to_addr_id,
            self.utils,
            self.factory
        )

        self.factory.to_tier_2_sales_order.assert_called_once()
        self.utils.create_sales_order_if_not_already_exists.assert_called_once()

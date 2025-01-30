import pytest
from paperless.client import PaperlessClient
from paperless.objects.orders import Order

from globalshop.exporter.exporter import GlobalShopOrderExporter
from globalshop.exporter.processors.order_line import OrderLineProcessor
from globalshop.tests.test_integration import GSIntegrationTestClass


class TestOrderProcessor:

    @pytest.fixture
    def order_processor(self) -> OrderLineProcessor:
        i = GSIntegrationTestClass()
        exporter = GlobalShopOrderExporter(i)
        return OrderLineProcessor(exporter=exporter)

    @pytest.fixture()
    def test_order(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        from globalshop.tests.get_test_order import get_test_order_json
        self.mock_order_json = get_test_order_json()
        return Order.from_json(self.mock_order_json)

    # def test_process_order(self, order_processor: OrderLineProcessor,
    #                        test_order: Order, mocker):
    #     from globalshop.tests.test_connection import mock_conn_client
    #     mock_conn_client(mocker)
    #     # order:Order = get_order(1)
    #     item = test_order.order_items[0]
    #     from globalshop.tests.test_customer import dummy_cust_record
    #     cus_rec = dummy_cust_record()
    #     order_processor._process(order=test_order, order_item=item,
    #                              line_number=1, customer_record=cus_rec)

import pytest

from globalshop.tests.test_integration import GSIntegrationTestClass
from paperless.client import PaperlessClient
from paperless.objects.orders import Order

from globalshop.exporter.processors.bom import BOMProcessor
from globalshop.exporter.exporter import GlobalShopOrderExporter
from globalshop.tests.test_connection import mock_conn_client


class FakeOrderComponent:
    pass


class TestRouterProcessor:

    @pytest.fixture
    def bom_processor(self) -> BOMProcessor:
        i = GSIntegrationTestClass()
        exporter = GlobalShopOrderExporter(i)
        return BOMProcessor(exporter=exporter)

    @pytest.fixture()
    def test_order(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        from globalshop.tests.get_test_order import get_test_order_json
        self.mock_order_json = get_test_order_json()
        return Order.from_json(self.mock_order_json)

    def test_process_bom(self, bom_processor: BOMProcessor,
                         test_order: Order, mocker):
        mock_conn_client(mocker)
        for item in test_order.order_items:
            bom_processor._process(item=item)

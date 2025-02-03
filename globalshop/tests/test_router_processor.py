import pytest
from paperless.client import PaperlessClient
from paperless.objects.orders import Order

from globalshop.exporter.processors.router import RouterProcessor
from globalshop.exporter.exporter import GlobalShopOrderExporter
from globalshop.tests.test_connection import mock_conn_client

from globalshop.tests.test_integration import GSIntegrationTestClass


class FakeOrderComponent:
    pass


class TestRouterProcessor:

    @pytest.fixture
    def router_processor(self) -> RouterProcessor:
        i = GSIntegrationTestClass()
        exporter = GlobalShopOrderExporter(i)
        return RouterProcessor(exporter=exporter)

    @pytest.fixture()
    def test_order(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        from globalshop.tests.get_test_order import get_test_order_json
        self.mock_order_json = get_test_order_json()
        return Order.from_json(self.mock_order_json)

    def test_process_router(self, router_processor: RouterProcessor,
                            test_order: Order, mocker):
        mock_conn_client(mocker)
        for item in test_order.order_items:
            router_processor._process(item=item)

    def test_get_product_line(self, router_processor: RouterProcessor):
        fake_oc = FakeOrderComponent()
        fake_oc.is_root_component = False
        line = router_processor._get_product_line(fake_oc)
        assert line == 'FC'

        fake_oc.is_root_component = True
        line = router_processor._get_product_line(fake_oc)
        assert line == 'FG'

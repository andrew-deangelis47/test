import pytest

from globalshop.exporter.exporter import GlobalShopOrderExporter
from globalshop.exporter.processors.part import PartProcessor
# from globalshop.tests.test_connection import mock_conn_client
from globalshop.client import GlobalShopClient
from globalshop.tests.test_integration import GSIntegrationTestClass
from paperless.client import PaperlessClient
from paperless.objects.orders import Order, OrderComponent

dummy_client = GlobalShopClient(server_name='test', database='dbq',
                                username='user1', password='pwd1')


class TestPartProcessor:

    @pytest.fixture
    def part_processor(self) -> PartProcessor:
        i = GSIntegrationTestClass()
        exporter = GlobalShopOrderExporter(i)
        return PartProcessor(exporter=exporter)

    @pytest.fixture
    def test_order(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        from globalshop.tests.get_test_order import get_test_order_json
        self.mock_order_json = get_test_order_json()
        return Order.from_json(self.mock_order_json)

    @pytest.fixture
    def hardware_component(self, test_order: Order):
        for comp in test_order.order_items[0].iterate_assembly():
            if comp.component.is_hardware:
                return comp.component

    def test_get_part_description(self, part_processor: PartProcessor,
                                  test_order: Order):
        line = test_order.order_items[0]
        component = line.components[0]

        description = part_processor._get_part_description(
            component=component, item=line, order=test_order)

        assert description == 'BASE PLATE'

    def test_get_purchased_component_part_description(
            self,
            part_processor: PartProcessor,
            test_order: Order,
            hardware_component: OrderComponent):
        line = test_order.order_items[0]

        description = part_processor._get_purchased_component_part_description(
            component=hardware_component, item=line)

        assert description == '1/4-20 PRESS FIT NUT SS PEM '

    def test_get_list_price(self,
                            part_processor: PartProcessor,
                            test_order: Order,
                            hardware_component: OrderComponent):
        line = test_order.order_items[0]
        component = line.components[0]

        list_price = part_processor._get_list_price(component=component,
                                                    item=line)
        assert list_price == 0

    def test_get_product_line(self,
                              part_processor: PartProcessor,
                              test_order: Order,
                              hardware_component: OrderComponent):
        line = test_order.order_items[0]
        component = line.components[0]

        pl = part_processor._get_product_line(component=component)
        assert pl == 'FC'

        pl = part_processor._get_product_line(component=line.root_component)
        assert pl == 'FG'

        pl = part_processor._get_product_line(component=hardware_component)
        assert pl == 'PP'

    def test_get_source(self, part_processor: PartProcessor,
                        test_order: Order,
                        hardware_component: OrderComponent):

        line = test_order.order_items[0]
        component = line.components[0]

        source = part_processor._get_source(component)
        assert source == 'F'

        source = part_processor._get_source(line.root_component)
        assert source == 'F'

        source = part_processor._get_source(hardware_component)
        assert source == 'J'

    # def test_process_part(self, part_processor: PartProcessor,
    #                       test_order: Order, mocker):
    #     mock_conn_client(mocker)
    #     line = test_order.order_items[0]
    #     component = line.components[0]
    #     part_processor._insert_component_part(root=line.root_component,
    #                                           component=component,
    #                                           line_item=line, order=test_order)

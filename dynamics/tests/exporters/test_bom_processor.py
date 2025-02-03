import pytest

from dynamics.tests.utils import DynamicsMock, add_costing_var, get_object_mocks, with_mocks

from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_quote
from types import SimpleNamespace

from dynamics.exceptions import DynamicsNotFoundException
from dynamics.exporter.processors.bom import BOMProcessor
from dynamics.objects.item import ProductionBOM, ProductionBOMItem, Item, ItemVariant


@pytest.fixture
def setup_integration():
    integration = Integration()
    from dynamics.exporter.exporter import DynamicsQuoteExporter
    exporter = DynamicsQuoteExporter(integration)
    return BOMProcessor(exporter)


basic_mocks = get_object_mocks({
    ProductionBOM: SimpleNamespace(
        No='new number',
        Name='new name'
    ),
    ProductionBOMItem: SimpleNamespace(
        No='num'
    ),
    Item: SimpleNamespace(
        No='num'
    ),
    ItemVariant: SimpleNamespace(
        No='num'
    )
})


class TestBOMProcessor:

    @staticmethod
    def process_bom(processor, item_num=0, component=None):
        component = component or get_quote(1, 1).quote_items[item_num].components[0]
        dynamics_customer = SimpleNamespace(
            No='No'
        )
        dynamics_part = SimpleNamespace(
            No='new number',
            Name='new name'
        )
        return processor._process(component, dynamics_part, dynamics_customer)

    def test_bom_exists(self, setup_integration):
        def run_test(call_data, get_args):
            self.process_bom(setup_integration)
            assert not call_data[ProductionBOM, 'create'].called
            assert not call_data[ProductionBOMItem, 'create'].called
        with_mocks(run_test, basic_mocks)

    def test_create_bom_no_materials(self, setup_integration):
        def run_test(call_data, get_args):
            self.process_bom(setup_integration)
            assert call_data[ProductionBOM, 'create'].called
            assert not call_data[ProductionBOMItem, 'create'].called
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(ProductionBOM, 'get_first', exception=DynamicsNotFoundException(''))
        ])

    def test_create_bom(self, setup_integration):
        def run_test(call_data, get_args):
            quote_component = get_quote(1, 1).quote_items[0].components[0]
            add_costing_var(quote_component, 'pp_mat_id_variable', 'test', setup_integration, material=True)
            add_costing_var(quote_component, 'pp_coating_item_id_var', 'test', setup_integration)
            self.process_bom(setup_integration, component=quote_component)
            assert call_data[ProductionBOM, 'create'].called
            assert call_data[ProductionBOMItem, 'create'].called
            assert get_args((ProductionBOMItem, 'create'))['No'] == 'test'
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(ProductionBOM, 'get_first', exception=DynamicsNotFoundException(''))
        ])

    def test_create_bom_r_part(self, setup_integration):
        def run_test(call_data, get_args):
            quote_component = get_quote(1, 1).quote_items[0].components[0]
            add_costing_var(quote_component, 'pp_r_part_flag', 'True', setup_integration)
            add_costing_var(quote_component, 'pp_surface_area_variable', 10, setup_integration)
            self.process_bom(setup_integration, component=quote_component)
            assert call_data[ProductionBOM, 'create'].called
            assert call_data[Item, 'create'].called
            assert call_data[ItemVariant, 'create'].called
            assert call_data[ProductionBOMItem, 'create'].called
            assert get_args((ItemVariant, 'create'))['TS_Unit_Weight'] == 10

        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(ProductionBOM, 'get_first', exception=DynamicsNotFoundException('')),
            DynamicsMock(Item, 'get_first', exception=DynamicsNotFoundException('')),
            DynamicsMock(ItemVariant, 'get_first', exception=DynamicsNotFoundException(''))
        ])

import pytest

from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_quote
from types import SimpleNamespace

from dynamics.exceptions import DynamicsNotFoundException
from dynamics.exporter.processors.part import PartProcessor
from dynamics.objects.item import Item
from dynamics.tests.utils import get_object_mocks, with_mocks, DynamicsMock


@pytest.fixture
def setup_integration():
    integration = Integration()
    from dynamics.exporter.exporter import DynamicsQuoteExporter
    exporter = DynamicsQuoteExporter(integration)
    processor = PartProcessor(exporter)
    return processor


basic_mocks = get_object_mocks({
    Item: SimpleNamespace(
        No='new number',
        Name='new name'
    )
})


class TestPartProcessor:

    @staticmethod
    def process_part(processor, quote_num=6):
        quote_component = get_quote(quote_num).quote_items[0].components[0]
        return processor._process(quote_component)

    def test_create_part(self, setup_integration):
        def run_test(call_data, get_args):
            self.process_part(setup_integration)
            assert call_data[Item, 'create'].called
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(Item, 'get_first', exception=DynamicsNotFoundException(''))
        ])

    def test_part_exists(self, setup_integration):
        def run_test(call_data, get_args):
            self.process_part(setup_integration)
            assert not call_data[Item, 'create'].called
        with_mocks(run_test, basic_mocks)

    def test_part_name_too_long(self, setup_integration):
        def run_test(call_data, get_args):
            part: Item = self.process_part(setup_integration, 4)
            assert len(part.No) <= 20
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(Item, 'get_first', exception=DynamicsNotFoundException(''))
        ])

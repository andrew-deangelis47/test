from types import SimpleNamespace

import pytest

from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_quote
from dynamics.exporter.processors.customer import CustomerProcessor
from dynamics.exporter.processors.part import PartProcessor
from dynamics.exporter.processors.bom import BOMProcessor
from dynamics.exporter.processors.process_map import ProcessMapProcessor
from dynamics.exporter.processors.routing import RoutingProcessor
from dynamics.exporter.processors.sales_quote import SalesQuoteProcessor, SalesQuoteLineProcessor
from dynamics.objects.item import ProductionBOMItem
from dynamics.tests.utils import with_mocks, DynamicsMock, get_object_mocks


@pytest.fixture
def setup_integration():
    integration = Integration()
    from dynamics.exporter.exporter import DynamicsQuoteExporter
    return DynamicsQuoteExporter(integration)


basic_mocks = [
    DynamicsMock(CustomerProcessor, '_process', return_val=(None, None)),
    DynamicsMock(SalesQuoteProcessor, '_process', return_val=None),
    DynamicsMock(SalesQuoteLineProcessor, '_process', return_val=None),
    DynamicsMock(PartProcessor, '_process', return_val=SimpleNamespace(
        No='TEST_NO'
    )),
    DynamicsMock(RoutingProcessor, '_process', return_val=None),
    DynamicsMock(BOMProcessor, '_process', return_val=(SimpleNamespace(
        No='TEST_NO'
    ), True)),
    DynamicsMock(ProcessMapProcessor, '_process', return_val=None),
    *get_object_mocks({
        ProductionBOMItem: None
    })
]


class TestDynamicsQuoteExport:
    def test_process_quote(self, setup_integration):
        def run_test(call_data, get_args):
            setup_integration._process_quote(get_quote(6))
            assert call_data[CustomerProcessor, '_process'].called
            assert call_data[PartProcessor, '_process'].called
            assert call_data[RoutingProcessor, '_process'].called
            assert call_data[BOMProcessor, '_process'].called
            assert call_data[ProcessMapProcessor, '_process'].called
            assert call_data[SalesQuoteProcessor, '_process'].called
            assert call_data[SalesQuoteLineProcessor, '_process'].called
        with_mocks(run_test, basic_mocks)

    def test_process_quote_with_assembly(self, setup_integration):
        def run_test(call_data, get_args):
            setup_integration._process_quote(get_quote(33))
            assert call_data[ProductionBOMItem, 'create'].called
            assert not call_data[ProductionBOMItem, 'get_with_filter_strings'].called
        with_mocks(run_test, basic_mocks)

    def test_process_quote_process_map_disabled(self, setup_integration):
        def run_test(call_data, get_args):
            setup_integration.erp_config.enable_ts_process_map = False
            setup_integration._process_quote(get_quote(6))
            assert call_data[CustomerProcessor, '_process'].called
            assert call_data[PartProcessor, '_process'].called
            assert call_data[RoutingProcessor, '_process'].called
            assert call_data[BOMProcessor, '_process'].called
            assert not call_data[ProcessMapProcessor, '_process'].called
            assert call_data[SalesQuoteProcessor, '_process'].called
            assert call_data[SalesQuoteLineProcessor, '_process'].called
        with_mocks(run_test, basic_mocks)

    def test_process_quote_failure(self, setup_integration):
        def run_test(call_data, get_args):
            with pytest.raises(Exception):
                setup_integration._process_quote(get_quote(33))
            assert call_data[setup_integration, 'send_email'].called
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(BOMProcessor, '_process', exception=Exception('unknown exception')),
            DynamicsMock(setup_integration, 'send_email', return_val=None),
        ])

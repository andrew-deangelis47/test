import pytest

from dynamics.tests.utils import DynamicsMock, add_costing_var, get_object_mocks, with_mocks

from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_quote
from types import SimpleNamespace

from dynamics.exceptions import DynamicsNotFoundException
from dynamics.exporter.processors.routing import RoutingProcessor
from dynamics.objects.item import Routing, RoutingOperation, MachineCenter, ProcessesAndOperations
from unittest.mock import create_autospec
from dynamics.api_error_handler import DynamicsApiErrorHandler


@pytest.fixture
def setup_integration():
    integration = Integration()
    from dynamics.exporter.exporter import DynamicsQuoteExporter
    exporter = DynamicsQuoteExporter(integration)
    return RoutingProcessor(exporter)


mock_dict = {
    Routing: SimpleNamespace(
        No='new number',
        Name='new name'
    ),
    RoutingOperation: SimpleNamespace(
        No='num'
    ),
    MachineCenter: SimpleNamespace(
        No='num',
        Name='mc'
    ),
    ProcessesAndOperations: SimpleNamespace(
        No='num'
    )
}

basic_mocks = get_object_mocks(mock_dict)


class TestRoutingProcessor:

    @staticmethod
    def process_routing(processor, item_num=3, component=None):
        component = component or get_quote(6).quote_items[item_num].components[0]
        api_error_handler = create_autospec(DynamicsApiErrorHandler)
        api_error_handler.handle_routing_update_error.return_value = None

        dynamics_part = SimpleNamespace(
            No='new number',
            Name='new name'
        )
        return processor._process(component, dynamics_part, api_error_handler)

    def test_routing_exists(self, setup_integration):
        def run_test(call_data, get_args):
            self.process_routing(setup_integration)
            assert not call_data[Routing, 'create'].called
            assert not call_data[RoutingOperation, 'create'].called
        with_mocks(run_test, basic_mocks)

    def test_create_routing_machine_center_not_found(self, setup_integration):
        def run_test(call_data, get_args):
            self.process_routing(setup_integration, item_num=3)
            assert get_args((RoutingOperation, 'create'), call_num=0)['Operation_No'] == '100'
            assert get_args((RoutingOperation, 'create'), call_num=1)['Operation_No'] == '200'
            assert not get_args((RoutingOperation, 'create'), call_num=0)['No']
            assert not get_args((RoutingOperation, 'create'), call_num=0)['TS_Operation_Name']
            assert call_data[Routing, 'create'].called
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(Routing, 'get_first', exception=DynamicsNotFoundException('')),
            DynamicsMock(MachineCenter, 'get_first', exception=DynamicsNotFoundException(''))
        ])

    def test_create_routing_no_machine_center(self, setup_integration):
        def run_test(call_data, get_args):
            quote_component = get_quote(6).quote_items[0].components[0]
            quote_component.shop_operations[0].costing_variables.clear()
            self.process_routing(setup_integration, item_num=0, component=quote_component)
            assert not call_data[RoutingOperation, 'create'].called
            assert call_data[Routing, 'create'].called
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(Routing, 'get_first', exception=DynamicsNotFoundException(''))
        ])

    def test_create_routing_with_process_name(self, setup_integration):
        def run_test(call_data, get_args):
            quote_component = get_quote(6).quote_items[3].components[0]
            add_costing_var(quote_component, 'pp_process_selection_variable', 'test', setup_integration)
            self.process_routing(setup_integration, item_num=3, component=quote_component)
            assert get_args((Routing, 'update'), arg_pos=0) == mock_dict[Routing].No
            assert get_args((Routing, 'update'), arg_pos=1)['TS_Process_Name'] == 'test'
            assert get_args((RoutingOperation, 'create'), call_num=0)['No'] == mock_dict[MachineCenter].No
            assert get_args((RoutingOperation, 'create'), call_num=0)['TS_Operation_Name'] \
                == mock_dict[MachineCenter].Name

        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(Routing, 'get_first', exception=DynamicsNotFoundException(''))
        ])

    def test_create_routing_processes_disabled(self, setup_integration):
        def run_test(call_data, get_args):
            setup_integration._exporter.erp_config.enable_ts_processes_and_operations = False
            quote_component = get_quote(6).quote_items[3].components[0]
            add_costing_var(quote_component, 'pp_process_selection_variable', 'test', setup_integration)
            self.process_routing(setup_integration, item_num=3, component=quote_component)
            assert not call_data[Routing, 'update'].called
            assert get_args((RoutingOperation, 'create'), call_num=0)['No'] == mock_dict[MachineCenter].No
            assert not get_args((RoutingOperation, 'create'), call_num=0)['TS_Operation_Name']
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(Routing, 'get_first', exception=DynamicsNotFoundException(''))
        ])

    def test_create_routing_operation_not_found(self, setup_integration):
        def run_test(call_data, get_args):
            self.process_routing(setup_integration, item_num=3)
            assert call_data[ProcessesAndOperations, 'create'].called
            assert get_args((RoutingOperation, 'create'), call_num=0)['No'] == mock_dict[MachineCenter].No
            assert get_args((RoutingOperation, 'create'), call_num=0)['TS_Operation_Name'] \
                == mock_dict[MachineCenter].Name
        with_mocks(run_test, [
            *basic_mocks,
            DynamicsMock(Routing, 'get_first', exception=DynamicsNotFoundException('')),
            DynamicsMock(ProcessesAndOperations, 'get_first', exception=DynamicsNotFoundException(''))
        ])

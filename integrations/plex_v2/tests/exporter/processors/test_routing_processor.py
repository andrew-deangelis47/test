from plex_v2.exporter.processors.routing import RoutingProcessor
from plex_v2.configuration import PlexConfig
from types import SimpleNamespace
from unittest.mock import create_autospec
from baseintegration.integration.integration_export_report import IntegrationExportReport
from paperless.objects.components import AssemblyComponent
from paperless.objects.orders import Order, OrderItem, OrderComponent, OrderOperation
from plex_v2.utils.export import ExportUtils
from plex_v2.factories.plex.part import PlexPartFactory
from plex_v2.factories.plex.part_operation import PartOperationFactory
from plex_v2.objects.operations_mapping import OperationsMapping
from plex_v2.objects.routing import PartOperation


class TestRoutingProcessor:

    def setup_method(self):
        integration_report = create_autospec(IntegrationExportReport)
        integration_report.update_table.return_value = True

        self.processor = RoutingProcessor(SimpleNamespace(
            erp_config=PlexConfig(
                routing_operation_to_ignore=['ignored_operation'],
                routing_datasource_properties_required=[],
                routing_datasource_properties_required_material=[]
            ),
            integration_report=integration_report
        ))

        self.part_factory = create_autospec(PlexPartFactory)

        self.pp_operation = create_autospec(OrderOperation)

        self.utils = create_autospec(spec=ExportUtils, name='utils')
        self.utils.get_non_ignored_operations_for_component.return_value = [self.pp_operation]

        self.order_component = create_autospec(OrderComponent)
        self.order_component.part_number = '1'
        self.order_component.material_operations = []

        self.part_operation = create_autospec(spec=PartOperation, name='part_operation')

        self.operation_factory = create_autospec(PartOperationFactory)
        self.operation_factory.to_part_operation.return_value = self.part_operation

        self.routing_update_datasource_factory = create_autospec(spec=RoutingProcessor, name='routing_update_datasource_factory')

        self.operations_mapping = create_autospec(OperationsMapping)
        self.operations_mapping.get_plex_op_code_from_pp_op_using_mapping_table.return_value = 'op'

        assembly_component = create_autospec(spec=AssemblyComponent, name='assembly_component')
        assembly_component.component = self.order_component

        order_item = create_autospec(OrderItem)
        order_item.iterate_assembly.return_value = [assembly_component]

        order = create_autospec(Order)
        order.order_items = [order_item]

        self.order = order

        return order

    def test_routing_processor_creates_routing_if_not_an_ignored_operation(self):
        self.pp_operation.operation_definition_name = 'not_ignored_op'
        self.order_component.shop_operations = [self.pp_operation]

        self.processor._process(
            self.order,
            self.utils,
            self.operation_factory,
            self.routing_update_datasource_factory,
            self.operations_mapping
        )

        self.part_operation.create.assert_called_once()

    def test_routing_processor_does_not_create_routing_if_ignored_operation(self):
        self.pp_operation.operation_definition_name = 'ignored_operation'
        self.order_component.shop_operations = [self.pp_operation]
        self.utils.get_non_ignored_operations_for_component.return_value = []

        self.processor._process(
            self.order,
            self.utils,
            self.operation_factory,
            self.routing_update_datasource_factory,
            self.operations_mapping
        )

        self.part_operation.create.assert_not_called()

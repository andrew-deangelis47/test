from plex_v2.exporter.processors.base import PlexProcessor
from typing import List
from plex_v2.objects.routing import PartOperation
from paperless.objects.orders import OrderItem, Order, OrderComponent, OrderOperation
from paperless.objects.components import AssemblyComponent
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from baseintegration.datamigration import logger
from plex_v2.utils.export import ExportUtils
from plex_v2.factories.plex.part_operation import PartOperationFactory
from plex_v2.factories.plex.part_operation_update_datasource import RoutingUpdateDatasourceFactory
from plex_v2.objects.operations_mapping import OperationsMapping
from plex_v2.objects.routing_upload_datasource import RoutingUploadDataSource


class RoutingProcessor(PlexProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'part_operations'

    def _process(self, order: Order, utils: ExportUtils, operation_factory: PartOperationFactory, routing_update_factory: RoutingUpdateDatasourceFactory, operations_mapping: OperationsMapping) -> PartOperation:
        # process routings for components
        self._process_component_routings(order, utils, operation_factory, routing_update_factory, operations_mapping)

        # process routings for material
        self._process_material_routings(order, utils, operation_factory, routing_update_factory, operations_mapping)

    def _process_material_routings(self, order: Order, utils: ExportUtils, operation_factory: PartOperationFactory, routing_update_factory: RoutingUpdateDatasourceFactory, operations_mapping: OperationsMapping) -> None:
        # iterate order lines
        order_item: OrderItem
        for order_item in order.order_items:

            # iterate components
            paperless_component: AssemblyComponent
            components: List[AssemblyComponent] = order_item.iterate_assembly()
            for paperless_component in components:
                paperless_component: OrderComponent = paperless_component.component

                # iterate material ops
                material_op: OrderOperation
                routings_created: List[PartOperation] = []
                ignored_operations: List[str] = []
                for material_op in paperless_component.material_operations:
                    op_num = utils.get_material_op_no(material_op)
                    material_routing: PartOperation = operation_factory.to_part_operation_from_material_operation(material_op, op_num)
                    # there wont neccesarily be an op defined on the material, if not just skip
                    if material_routing is None:
                        continue

                    # increment the count of created routings
                    already_exists = self._create_routing_if_not_exists(material_routing)
                    if already_exists:
                        ignored_operations.append(material_op.operation_definition_name)
                    else:
                        # get the associated plex op code
                        plex_op_code = operations_mapping.get_plex_op_code_from_op_id(material_routing.operationId)
                        routings_created.append(plex_op_code)

                        # if data source properties are required set them
                        if len(self.config.routing_datasource_properties_required_material) > 0:
                            routing_update_datasource: RoutingUploadDataSource = routing_update_factory.to_material_operation_datasource(
                                material_operation=material_op,
                                operation_number=op_num
                            )
                            routing_update_datasource.create()

                # log the routings in the integration report for this part
                self._log_created_routings_for_part(paperless_component, routings_created)

    def _process_component_routings(self, order: Order, utils: ExportUtils, operation_factory: PartOperationFactory, routing_update_factory: RoutingUpdateDatasourceFactory, operations_mapping: OperationsMapping) -> None:
        # iterate order lines
        order_item: OrderItem
        for order_item in order.order_items:

            # iterate components
            paperless_component: AssemblyComponent
            components: List[AssemblyComponent] = order_item.iterate_assembly()
            for paperless_component in components:
                paperless_component: OrderComponent = paperless_component.component

                # get the plex part by number and rev
                plex_part = utils.get_plex_part_from_paperless_component(paperless_component)

                # set the starting operation number and the increment based on config
                operation_increment_number = self.config.part_operation_increment_step
                op_num = operation_increment_number

                # iterate shop operations
                paperless_op: OrderOperation
                routings_created: List[PartOperation] = []
                ignored_operations: List[str] = []
                valid_operations = utils.get_non_ignored_operations_for_component(paperless_component)
                total_ops = len(valid_operations)
                op_count = 1
                for paperless_op in valid_operations:

                    # create the routing
                    plex_part_routing: PartOperation = operation_factory.to_part_operation(
                        plex_part=plex_part,
                        pp_op=paperless_op,
                        operation_number=op_num,
                        is_last_op=total_ops == op_count
                    )

                    # increment the count of created routings
                    already_exists = self._create_routing_if_not_exists(plex_part_routing)
                    if already_exists:
                        ignored_operations.append(paperless_op.operation_definition_name)
                    else:
                        # get the associated plex op code
                        plex_op_code = utils.get_plex_operation_code_from_paperless_operation(paperless_op, operations_mapping)
                        routings_created.append(plex_op_code)

                        # if data source properties are required, set those
                        if len(self.config.routing_datasource_properties_required) > 0:
                            routing_update_datasource: RoutingUploadDataSource = routing_update_factory.to_part_operation_datasource(
                                plex_part=plex_part,
                                pp_op=paperless_op,
                                operation_number=op_num
                            )
                            routing_update_datasource.create()

                    op_num += operation_increment_number
                    op_count += 1

                # log the routings in the integration report for this part
                self._log_created_routings_for_part(paperless_component, routings_created, ignored_operations)

    def _log_created_routings_for_part(self, component: OrderComponent, routings_created: List[str], ignored_operations: List[str] = []) -> None:
        if len(routings_created) > 0:
            self._add_report_message(f'Created {len(routings_created)} routing lines for part {component.part_number}: ({", ".join(routings_created)})')

        if len(ignored_operations) > 0:
            self._add_report_message(f'Ignored or already existing operations for part {component.part_number}: {", ".join(ignored_operations)}')

    def _create_routing_if_not_exists(self, routing: PartOperation) -> PartOperation:
        """
        handles the case where we try to create a duplicate routing step
        for instance, if the first export fails and we try again
        returns whether the op exsisted or not
        """
        try:
            routing.create()
            return False
        except Exception as e:
            if 'FIELD_REFERENCE_YIELDS_DUPLICATE' in e.message:
                logger.info(f'Routing {routing.operationNumber} will create a duplicate, skipping')
                return True

            else:
                raise CancelledIntegrationActionException(f'While Creating Routing: {e.message}')

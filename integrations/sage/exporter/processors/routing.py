from baseintegration.datamigration import logger
from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order, OrderItem, OrderOperation

from sage.models.converters.routing_export.pp_routing_header_to_sage_routing_header import \
    PaperlessRoutingHeaderToSageRoutingHeader
from sage.models.converters.routing_export.pp_routing_op_to_sage_routing_op import PaperlessRoutingOpToSageRoutingOp
from sage.models.converters.routing_export.pp_routing_scheduling_to_sage_routing_scheduling import \
    PaperlessRoutingSchToSageRoutingSch
from sage.models.sage_models.routing import RoutingFullEntity
from sage.sage_api.client import SageImportClient


class RoutingProcessor(BaseProcessor):

    def _process(self, order: Order) -> list:
        logger.info('----- ROUTING PROCESSOR -------------')
        for item in order.order_items:
            self.should_populate_routing_on_part_from_paperless_operations(item)
        logger.info(f'--------- processed {len(order.order_items)} for routing --------------------')

    def should_populate_routing_on_part_from_paperless_operations(self, item: OrderItem):
        for component in item.components:
            if component.type == 'manufactured':
                logger.info(f'components is manufactured! process routing for {component.part_number}')
                self.process_routing_for_component(component=component, item=item)
            else:
                logger.info('component is not purchased or assembly, dont process')
        return

    def process_routing_for_component(self, component, item):
        routing_header = self.populate_routing_header(component, item)
        routing_operations = self.populate_routing_operations(component, item)
        routing_operations_length = len(routing_operations)
        routing_schedulings = self.populating_routing_scheduling(routing_operations_length)

        self.make_routing_query(routing_header, routing_operations, routing_schedulings)

    def populate_routing_header(self, component, item):
        part_number = str(component.part_number)
        part_name = str(component.part_name)
        pp_routing_header = {
            'entity_type': 'E',
            'routing': part_number,
            'routing_code': '40',
            'site': 'ARC01',
            'header_title': part_name,
            'use_status': '2',
            'valid_from': '0',
            'valid_to': '0',
            'time_unit': '1',
            'wo_management_mode': '4',
            'header_text_0': '',
            'header_text_1': '',
            'header_text_2': '',
            'major_version': '',
            'minor_version': '',
            'default_rou_code': '',
            'option': ''
        }
        sage_routing_header = PaperlessRoutingHeaderToSageRoutingHeader.to_sage_routing_header(self, pp_routing_header)
        return sage_routing_header

    def populate_routing_operations(self, component, item):
        routing_lines = []
        op_num = 10
        for operation in component.shop_operations:
            if operation.is_outside_service:
                routing_line = self.create_routing_line_from_outside_service(op_num, operation, component, item)
            else:
                routing_line = self.create_routing_line_from_inside_service(op_num, operation, component, item)
            routing_lines.append(routing_line)
            op_num += 10
        return routing_lines

    def get_standard_op_and_work_center_id(self, operation: OrderOperation):

        work_center_id = operation.get_variable('work_center_id')

        return work_center_id

    def create_routing_line_from_outside_service(self, op_num, operation, component, item):
        run_time = str(operation.runtime)
        set_up_time = str(operation.setup_time)
        work_center = self.get_standard_op_and_work_center_id(operation)
        op_description = str(operation.name).replace('|', '')
        op_num = str(op_num)
        pp_routing_op = {
            'entity_type': 'L',
            'operation': op_num,
            'alternate_index': '',
            'start_date': '',
            'end_date': '',
            'standard_op': '10',
            'main_work_center': work_center,
            'labor_work_center': '',
            'labor_time_set_fac': '',
            'labor_r_time_fact': '',
            'ope_description': op_description,
            'operation_uom': 'EA',
            'stk_ope_converstion': '',
            'number_of_resources': '1',
            'number_labor_res': '',
            'percent_efficiency': '100.000',
            'shrinkage_in_percentage': '',
            'run_time_code': 'Proportional',
            'management_unit': 'Time for 1',
            'base_quantity': '1.000',
            'preparation_time': '',
            'setup_time': '0.0160',
            'run_time': run_time,
            'rate': set_up_time,
            'waiting_time': '',
            'post_run_time': '',
            'subcontract': 'No',
            'subcontract_prod': ' ',
            'operation_text_1': '',
            'operation_text_2': '',
            'operation_text_3': ''
        }
        sage_routing_op = PaperlessRoutingOpToSageRoutingOp.to_sage_routing_op(self, pp_routing_op)
        return sage_routing_op

    def create_routing_line_from_inside_service(self, op_num, operation, component, item):
        run_time = str(operation.runtime)
        set_up_time = str(operation.setup_time)
        op_description = str(operation.name).replace('|', '')

        work_center = self.get_standard_op_and_work_center_id(operation)

        op_num = str(op_num)
        pp_routing_op = {
            'entity_type': 'L',
            'operation': op_num,
            'alternate_index': '',
            'start_date': '',
            'end_date': '',
            'standard_op': '10',
            'main_work_center': work_center,
            'labor_work_center': '',
            'labor_time_set_fac': '',
            'labor_r_time_fact': '',
            'ope_description': op_description,
            'operation_uom': 'EA',
            'stk_ope_converstion': '',
            'number_of_resources': '1',
            'number_labor_res': '',
            'percent_efficiency': '100.000',
            'shrinkage_in_percentage': '',
            'run_time_code': 'Proportional',
            'management_unit': 'Time for 1',
            'base_quantity': '1.000',
            'preparation_time': '',
            'setup_time': '0.0160',
            'run_time': run_time,
            'rate': set_up_time,
            'waiting_time': '',
            'post_run_time': '',
            'subcontract': 'No',
            'subcontract_prod': ' ',
            'operation_text_1': '',
            'operation_text_2': '',
            'operation_text_3': ''
        }
        sage_routing_op = PaperlessRoutingOpToSageRoutingOp.to_sage_routing_op(self, pp_routing_op)
        return sage_routing_op

    def populating_routing_scheduling(self, routing_operations_length):
        operation_no = 10
        downstream_no = 20
        count = 0
        routing_scheduling_conv_models = []
        while count is not routing_operations_length:
            if count is routing_operations_length - 1:
                downstream_no = 0
            pp_routing_scheduling = {
                'entity_type': 'S',
                'operation': str(operation_no),
                'downstream_operation': str(downstream_no),
                'milestone': 'Normal Tracking',
                'production_step': 'No',
                'scheduling': 'Absolute Successor',
                'overlapping_time': '',
                'overlapping_qty': '',
                'number_of_overlap_lots': ''
            }
            sage_routing_schedule = PaperlessRoutingSchToSageRoutingSch.to_sage_routing_sch(self, pp_routing_scheduling)
            routing_scheduling_conv_models.append(sage_routing_schedule)
            operation_no += 10
            downstream_no += 10
            count += 1
        return routing_scheduling_conv_models

    def make_routing_query(self, routing_header, routing_operations, routing_schedulings):
        full_routing_entity = RoutingFullEntity \
            .get_routing_header_and_routing_op_and_routing_sheduling_return_full_routing(self, routing_header,
                                                                                         routing_operations,
                                                                                         routing_schedulings)

        full_routing_entity.replace(';', ',')
        client = SageImportClient.get_instance()

        client.create_routing(full_routing_entity)

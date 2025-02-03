from typing import Optional

from paperless.objects.quotes import QuoteComponent

from baseintegration.exporter.quote_exporter import logger

from dynamics.utils import DynamicsExportProcessor
from dynamics.exceptions import DynamicsNotFoundException, DynamicsException
from dynamics.objects.item import Item, Routing, RoutingOperation, MachineCenter, ProcessesAndOperations
from dynamics.api_error_handler import DynamicsApiErrorHandler


class RoutingProcessor(DynamicsExportProcessor):

    def _process(self, component: QuoteComponent, item: Item, api_error_handler: DynamicsApiErrorHandler) -> Routing:
        routing: Routing
        try:
            routing = Routing.get_first({
                'No': item.No
            })
        except DynamicsNotFoundException:
            routing = Routing.create({
                'No': item.No
            })
            self._create_routing_lines(routing, component, item, api_error_handler)

        return routing

    def _create_routing_lines(self, routing: Routing, component: QuoteComponent, item: Item, api_error_handler: DynamicsApiErrorHandler):
        current_operation_num = 100
        for operation in component.shop_operations:
            machine_center_no = self.get_operation_variable(operation, 'pp_machine_center_variable')
            process_name = self.get_quantity_operation_variable(operation, 'pp_process_selection_variable',
                                                                component)
            enable_ts_processes_and_operations = self.get_config_value('enable_ts_processes_and_operations')

            if enable_ts_processes_and_operations and process_name:
                logger.info(f'Setting routing process name to {process_name}')

                # update the routing, handle the exception if there is one
                try:
                    Routing.update(item.No, {
                        'TS_Process_Name': process_name
                    })
                except DynamicsException as ex:
                    api_error_handler.handle_routing_update_error(ex, component)

            if not machine_center_no:
                logger.info(f'Machine center not found on operation {operation.name}, skipping export')
                continue

            machine_center: Optional[MachineCenter] = None
            operation_name: Optional[str] = None

            try:
                machine_center = MachineCenter.get_first({
                    'No': machine_center_no
                })
                if enable_ts_processes_and_operations:
                    operation_name = machine_center.Name or machine_center.No
                    ProcessesAndOperations.get_or_create({
                        'Type': 'Operation',
                        'Description': operation_name
                    })
            except DynamicsNotFoundException:
                logger.info(f'Could not find machine center in Dynamics: {machine_center_no}')

            RoutingOperation.create({
                "Operation_No": str(current_operation_num),
                "Routing_No": routing.No,
                "Type": "Machine Center",
                "No": machine_center and machine_center.No,
                'TS_Operation_Name': operation_name,
                "Setup_Time": operation.setup_time,
                "Run_Time": operation.runtime
            })

            current_operation_num += 100

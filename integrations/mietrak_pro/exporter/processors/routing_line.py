from typing import Union, Optional

from baseintegration.utils.operations import OperationUtils
from mietrak_pro.query.router import create_routing_line, get_work_center_from_description, get_work_center_from_pk, \
    get_operation_from_pk
from mietrak_pro.query.part import create_item, get_item, get_item_type, get_calculation_type, get_unit_of_measure_set

from mietrak_pro.models import Party, Operation
from mietrak_pro.exporter.processors import MietrakProProcessor
from mietrak_pro.exporter.utils import RoutingLinesData
from baseintegration.datamigration import logger
from paperless.custom_tables.custom_tables import CustomTable
from mietrak_pro.exporter.utils import BillOfMaterial
from paperless.objects.orders import OrderComponent
from paperless.objects.quotes import QuoteComponent

from integrations.mietrak_pro.query.router import create_default_work_center
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException

MINUTES_PER_HOUR = 60.
PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_WORK_CENTER_MAPPING = None
PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_OUTSIDE_SERVICE_ITEM_MAPPING = None
SKIP_LIST = None
import math


class RoutingLineProcessor(MietrakProProcessor):
    do_rollback = False

    def __init__(self, exporter):
        super().__init__(exporter)
        self.component = None

    def _process(self, router, component: Union[OrderComponent, QuoteComponent], customer):
        self.component = component
        # Create a routing line for every operation on the Paperless Parts component, unless it's in the skip list
        routing_lines = []
        for operation in component.shop_operations:
            if self.should_skip_operation(operation):
                continue

            if operation.is_outside_service:
                routing_line = self.create_outside_service_routing_line(operation, router, customer)
            else:
                routing_line = self.create_inside_operation_routing_line(operation, router)

            if routing_line is not None:
                routing_lines.append(routing_line)

        routing_lines_data = RoutingLinesData(routing_lines=tuple(routing_lines))
        return routing_lines_data

    def create_inside_operation_routing_line(self, operation, router):
        runtime_minutes = self.get_runtime_minutes(operation)
        setup_time_minutes = self.get_setup_time_minutes(operation)
        pieces_per_hour = self.get_pieces_per_hour(runtime_minutes)
        operation_notes = operation.notes

        work_center = self.get_work_center_for_operation(operation)
        mtp_operation = self.get_operation(operation)
        if work_center is None:
            work_center = self.get_or_create_default_work_center()
            if work_center is None:
                return None
            preamble = f'Could not find work center corresponding to PP op {operation.name} - please update the mapping.'
            if operation_notes is not None:
                operation_notes = f'{preamble} \n\n{operation_notes}'
            else:
                operation_notes = preamble

        logger.info(f'Creating routing line {work_center.description} for part number {router.partnumber}')
        routing_line = \
            create_routing_line(router, work_center, runtime_minutes, setup_time_minutes, pieces_per_hour,
                                operation_notes, mtp_operation)
        return routing_line

    def get_pieces_per_hour(self, runtime_minutes):
        if runtime_minutes:
            pieces_per_hour = MINUTES_PER_HOUR / runtime_minutes
        else:
            pieces_per_hour = None
        return pieces_per_hour

    def get_setup_time_minutes(self, operation):
        if operation.setup_time is not None:
            setup_time_minutes = operation.setup_time * MINUTES_PER_HOUR
            setup_time_minutes = self._exporter.get_value_relative_to_current_node(setup_time_minutes)
        else:
            setup_time_minutes = 0
        return math.ceil(setup_time_minutes)

    def get_runtime_minutes(self, operation):
        if operation.runtime is not None:
            runtime_minutes = operation.runtime * MINUTES_PER_HOUR
        else:
            runtime_minutes = None
        return runtime_minutes

    def should_skip_operation(self, operation):
        should_skip = False
        operation_skip_list = self.get_operation_skip_list()
        if operation.name in operation_skip_list or \
                operation.operation_definition_name and operation.operation_definition_name in operation_skip_list:
            should_skip = True
            logger.info(f'Skipping operation {operation.name} because it is in the skip list')
        return should_skip

    def get_work_center_for_operation(self, operation):
        if self._exporter.erp_config.pp_work_center_pk_var:
            work_center_pk = operation.get_variable(self._exporter.erp_config.pp_work_center_pk_var)
            if not work_center_pk:
                return None
            work_center = get_work_center_from_pk(int(float(work_center_pk)))
        else:
            work_center_description = self.map_pp_op_to_mietrak_pro_work_center(operation)
            if work_center_description is None:
                return None
            work_center = get_work_center_from_description(work_center_description)
        return work_center

    def get_operation(self, operation) -> Optional[Operation]:
        if self._exporter.erp_config.pp_operation_pk_var:
            operation_pk = operation.get_variable(self._exporter.erp_config.pp_operation_pk_var)
            if not operation_pk:
                return None
            return get_operation_from_pk(int(float(operation_pk)))

    def map_pp_op_to_mietrak_pro_work_center(self, operation):
        PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_WORK_CENTER_MAPPING = \
            self.get_paperless_parts_operation_to_mietrak_pro_work_center_mapping()
        work_center_description = PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_WORK_CENTER_MAPPING.get(operation.name, None)
        if work_center_description is None:
            work_center_description = PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_WORK_CENTER_MAPPING.get(
                operation.operation_definition_name, None)
        return work_center_description

    def get_paperless_parts_operation_to_mietrak_pro_work_center_mapping(self):
        global PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_WORK_CENTER_MAPPING
        if PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_WORK_CENTER_MAPPING is None:
            PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_WORK_CENTER_MAPPING = {}
            try:
                operation_mapping_table_details = CustomTable.get('operation_to_work_center_mapping')
                rows = operation_mapping_table_details['rows']
                for row in rows:
                    PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_WORK_CENTER_MAPPING[
                        row['paperless_parts_operation_name']] = \
                        row['work_center_description']
            except Exception as e:
                logger.error(f'Encountered an error fetching the operation to work center mapping: {e}')
        return PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_WORK_CENTER_MAPPING

    def get_or_create_default_work_center(self):
        work_center_description = self._exporter.erp_config.default_work_center_name
        if not work_center_description:
            return None
        work_center_code = self._exporter.erp_config.default_work_center_code
        default_work_center = get_work_center_from_description(work_center_description)
        if default_work_center is None:
            logger.info(f'Creating new default work center {work_center_description}')
            default_work_center = create_default_work_center(work_center_code, work_center_description,
                                                             self._exporter.division_pk)
        return default_work_center

    def get_operation_skip_list(self):
        global SKIP_LIST  # Use a module level variable so we only make one request to pull down the table
        if SKIP_LIST is None:
            SKIP_LIST = []
            try:
                skip_list_mapping_table_details = CustomTable.get('operation_skip_list')
                rows = skip_list_mapping_table_details['rows']
                for row in rows:
                    SKIP_LIST.append(row['paperless_parts_operation_name'])
            except Exception as e:
                logger.error(f'Encountered an error fetching the operation skip list: {e}')
        return SKIP_LIST

    def create_outside_service_routing_line(self, operation, router, customer):
        runtime_minutes = 0.
        setup_time_minutes = 0.
        pieces_per_hour = None
        operation_notes = operation.notes

        work_center = self.get_work_center_for_outside_service(operation)
        mtp_operation = self.get_operation(operation)
        if work_center is None:
            work_center = self.get_or_create_default_outside_service_work_center()
            if work_center is None:
                return work_center

        logger.info(
            f'Creating outside service routing line {work_center.description} for part number {router.partnumber}')
        routing_line = \
            create_routing_line(router, work_center, runtime_minutes, setup_time_minutes, pieces_per_hour,
                                operation_notes, mtp_operation)

        # In MIE Trak Pro, outside services are represented in the Item table. This item should be tied
        # to the outside service routing line
        outside_service_item = self.get_or_create_outside_service_item(operation, customer)
        if outside_service_item is None:
            preamble = f'Could not find outside service item corresponding to PP op {operation.name} - please update the mapping.'
            if operation_notes is not None:
                operation_notes = f'{preamble} \n\n{operation_notes}'
            else:
                operation_notes = preamble
            routing_line.comment = operation_notes
            routing_line.save()
        else:
            # Link the outside service item to the router, specifying the sequence number of the routing line created above
            bom_processor = self._exporter.get_processor_instance(BillOfMaterial)
            bom_processor.component = self.component
            outside_service_item_bom_quantity = 1.  # TODO - is this a valid assumption?
            sequence_number = routing_line.sequencenumber
            logger.info(
                f'Creating BOM Item link for parent {router.partnumber} and child {outside_service_item.partnumber}')
            bom_item_link = bom_processor.create_bom_item_link(router, outside_service_item,
                                                               outside_service_item_bom_quantity,
                                                               sequence_number)
            osv_price = self._exporter.erp_config.osv_piece_price_variable_name
            for i, qty in enumerate(operation.quantities):
                var_obj = OperationUtils.get_variable_obj(operation, osv_price, qty.quantity)
                val = var_obj.value if var_obj else 0
                if i == 0:
                    bom_item_link.price = val
                    bom_item_link.quantity1 = qty.quantity
                else:
                    setattr(bom_item_link, f'price{i + 1}', val)
                    setattr(bom_item_link, f'quantity{i + 1}', qty.quantity)
            bom_item_link.save()
        return routing_line

    def get_work_center_for_outside_service(self, operation):
        # Leave this as a placeholder in case a customer has more complicated logic for assigning outside service work
        # centers. Currently we assume that there is a single outside service work center that is used for all outside
        # services
        if self._exporter.erp_config.pp_work_center_pk_var:
            work_center_pk = operation.get_variable(self._exporter.erp_config.pp_work_center_pk_var)
            if not work_center_pk:
                return None
            work_center = get_work_center_from_pk(int(float(work_center_pk)))
            return work_center

    def get_or_create_default_outside_service_work_center(self):
        work_center_description = self._exporter.erp_config.default_outside_service_work_center_name
        if not work_center_description:
            return None
        work_center_code = self._exporter.erp_config.default_outside_service_work_center_code
        default_work_center = get_work_center_from_description(work_center_description)
        if default_work_center is None:
            logger.info(f'Creating new default outside service work center {work_center_description}')
            default_work_center = create_default_work_center(work_center_code, work_center_description,
                                                             self._exporter.division_pk)
        return default_work_center

    def get_or_create_outside_service_item(self, operation, customer):
        outside_service_item_part_number, outside_service_item_revision = \
            self.map_pp_op_to_mietrak_pro_outside_service_item(operation)
        if outside_service_item_part_number is None:
            return None
        outside_service_item = get_item(outside_service_item_part_number, outside_service_item_revision)
        if outside_service_item is not None:
            logger.info(
                f'Found existing outside service Item record for part number {outside_service_item_part_number} and revision {outside_service_item_revision}')
        else:
            logger.info(
                f'Did not find existing outside service Item record for part number {outside_service_item_part_number} and revision {outside_service_item_revision}. Creating new record.')
            description = RoutingLineProcessor.get_outside_service_item_description(operation)
            assigned_party = self.get_party(customer, operation)
            is_itar = False
            item_type = RoutingLineProcessor.get_outside_service_item_type()
            calculation_type = RoutingLineProcessor.get_outside_service_item_calc_type(item_type)
            general_ledger_account = RoutingLineProcessor.get_outside_service_item_general_ledger_account()
            item_class = None
            unit_of_measure_set = RoutingLineProcessor.get_outside_service_item_unit_of_measure_set()

            # Create a new outside service item with the supplied part number and revision
            outside_service_item = create_item(outside_service_item_part_number,
                                               outside_service_item_revision,
                                               description,
                                               assigned_party,
                                               is_itar,
                                               item_type,
                                               calculation_type,
                                               general_ledger_account,
                                               item_class,
                                               unit_of_measure_set, self._exporter.division_pk)
        return outside_service_item

    def get_party(self, customer, operation):
        """ All Item records in MIE Trak Pro need to be associated with a Party. Attempt to assign the Party for this
            Item based on the Party name supplied in the config, but fall back to the customer if no match is found. """
        party_name = self._exporter.erp_config.default_outside_service_item_vendor_name
        if self._exporter.erp_config.outside_service_item_vendor_variable:
            party_name = operation.get_variable(self._exporter.erp_config.outside_service_item_vendor_variable)
        assigned_party = customer
        outside_service_item_vendor_party = Party.objects.filter(name=party_name).first()
        if outside_service_item_vendor_party is not None:
            assigned_party = outside_service_item_vendor_party
            logger.info(f'Got outside service vendor -> {assigned_party.name}')
        return assigned_party

    @staticmethod
    def get_outside_service_item_description(operation):
        description = operation.notes
        return description

    @staticmethod
    def get_outside_service_item_type():
        component_type = 'purchased'
        is_raw_material = False
        is_outside_process = True
        item_type = get_item_type(component_type, is_raw_material, is_outside_process)
        return item_type

    @staticmethod
    def get_outside_service_item_calc_type(item_type: str):
        return get_calculation_type(item_type)

    @staticmethod
    def get_outside_service_item_general_ledger_account():
        """ Take component, order_item, and order as arguments because it's not clear what information
            in Paperless we'll need to map to MIE Trak Pro's General Ledger Account. """
        return None

    @staticmethod
    def get_outside_service_item_unit_of_measure_set():
        unit_of_measure_set_code = 'EACH'
        return get_unit_of_measure_set(unit_of_measure_set_code)

    def map_pp_op_to_mietrak_pro_outside_service_item(self, operation):
        # Assume that outside service items don't have revisions. If they do, override this method as well as the
        # method that constructs the mapping
        outside_service_item_revision = None
        outside_service_item_part_number = None
        if self._exporter.erp_config.pp_outside_process_var:
            process_var = OperationUtils.get_variable_obj(operation,
                                                          self._exporter.erp_config.pp_outside_process_var)
            if process_var:
                if 'PartNumber' not in process_var.row:
                    logger.error("Cancelling action since outside service P3L var is not set")
                    raise CancelledIntegrationActionException("Outside Service not selected")
                outside_service_item_part_number = process_var.row['PartNumber']
        else:
            PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_OUTSIDE_SERVICE_ITEM_MAPPING = \
                RoutingLineProcessor.get_paperless_parts_operation_to_mietrak_pro_outside_service_item_mapping()
            outside_service_item_part_number = PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_OUTSIDE_SERVICE_ITEM_MAPPING.get(
                operation.name, None)
            if outside_service_item_part_number is None:
                name = operation.operation_definition_name
                outside_service_item_part_number = \
                    PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_OUTSIDE_SERVICE_ITEM_MAPPING.get(name, None)
        return outside_service_item_part_number, outside_service_item_revision

    @staticmethod
    def get_paperless_parts_operation_to_mietrak_pro_outside_service_item_mapping():
        global PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_OUTSIDE_SERVICE_ITEM_MAPPING
        if PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_OUTSIDE_SERVICE_ITEM_MAPPING is None:
            PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_OUTSIDE_SERVICE_ITEM_MAPPING = {}
            try:
                operation_mapping_table_details = CustomTable.get('operation_to_outside_service_item_mapping')
                rows = operation_mapping_table_details['rows']
                for row in rows:
                    PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_OUTSIDE_SERVICE_ITEM_MAPPING[
                        row['paperless_parts_operation_name']] = \
                        row['outside_service_item_part_number']
            except Exception as e:
                logger.error(f'Encountered an error fetching the operation to work center mapping: {e}')
        return PAPERLESS_PARTS_OPERATION_TO_MIETRAK_PRO_OUTSIDE_SERVICE_ITEM_MAPPING

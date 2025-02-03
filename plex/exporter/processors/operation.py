import re

from paperless.objects.orders import OrderOperation

from baseintegration.datamigration import logger
from plex.configuration import OP_INCREMENT
from plex.exceptions import PlexException
from plex.exporter.processors.base import PlexProcessor
from plex.objects.routing import PartOperation, Operation


class OperationProcessor(PlexProcessor):

    def get_operation_type(self, order_op: OrderOperation) -> str:
        """
        This method will search the costing variables of the paperless parts operations based on configuration
        options for PLEX operation type.

        @param order_op : The paperless parts order shop operation that is being converted to a PLEX router step
        @type order_op : OrderOperation

        @return: The PLEX operation types
        @rtype: str
        """
        op_type = self._exporter.erp_config.default_part_operation_type
        costing_variable = self._exporter.erp_config.costing_variable_operation_type
        if costing_variable and costing_variable != '':
            costing_variable_value = order_op.get_variable(costing_variable)
            if costing_variable_value and costing_variable_value != '':
                op_type = costing_variable_value
        return op_type

    def get_operation_increment_step(self) -> int:
        """
        Get the step interval for spacing out operations.

        @return: part operation increment step
        @rtype: int
        """
        increment_step = int(self._exporter.erp_config.part_operation_increment_step)
        if increment_step is None or increment_step <= 0:
            increment_step = OP_INCREMENT
        return increment_step

    def _create_part_op(self, op_code, part_id, index, multi_op_indices, op_type):
        for match in re.finditer(r'{([a-zA-Z_]+)}', op_code):
            var_name = match.group(1)
            if var_name not in multi_op_indices:
                multi_op_indices[var_name] = 1
            else:
                multi_op_indices[var_name] = multi_op_indices[var_name] + 1
        plex_op_code = op_code.format(**multi_op_indices)
        ops = Operation.find_operations(code=plex_op_code)
        if len(ops) == 0:
            raise PlexException(f'No suitable operation in Plex found for `{op_code}`')
        op: Operation = ops[0]
        increment_step = self.get_operation_increment_step()
        part_op = PartOperation(
            operationId=op.id,
            operationNumber=index * increment_step,
            partId=part_id,
            type=op_type,
            active=False,
            subOperation=False,
            shippable=False,
        )
        logger.info('PartOperation successfully created with op code {}'.format(plex_op_code))
        return part_op

    def _process(self, order_op: OrderOperation, operation_mapping: dict, part_id: str, index: int,
                 multi_op_indices: dict, create=True) -> PartOperation:

        op_type = self.get_operation_type(order_op=order_op)

        for row in operation_mapping:
            paperless_operation_name = self._exporter.erp_config.paperless_operation_name_column_header
            if row[paperless_operation_name] != '' and (row[paperless_operation_name] in order_op.name or row[paperless_operation_name] in order_op.operation_definition_name):
                if 'Paperless_Only' in row and row['Paperless_Only']:
                    return None
                else:
                    plex_op_code = row[self._exporter.erp_config.plex_operation_code_column_header]
                    logger.info('Mapping found: {} -> {}'.format(order_op.name, plex_op_code))
                    part_op = self._create_part_op(plex_op_code, part_id, index, multi_op_indices, op_type)
                    if create:
                        return part_op.create()
                    else:
                        return part_op

        # if no table entry is found...
        part_op = self._create_part_op(order_op.operation_definition_name, part_id, index, multi_op_indices, op_type)
        if create:
            return part_op.create()
        else:
            return part_op

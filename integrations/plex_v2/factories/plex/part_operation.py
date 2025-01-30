from plex_v2.objects.routing import PartOperation
from plex_v2.objects.part import Part
from paperless.objects.orders import OrderOperation
from plex_v2.factories.base import BaseFactory
from plex_v2.objects.operations_mapping import OperationsMapping
from plex_v2.configuration import PlexConfig
from plex_v2.utils.export import ExportUtils
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


class PartOperationFactory(BaseFactory):

    operations_mapping: OperationsMapping

    def __init__(self, config: PlexConfig, operations_mapping: OperationsMapping, utils: ExportUtils):
        self.config = config
        self.operations_mapping = operations_mapping
        self.utils = utils

    def to_part_operation_from_material_operation(self, material_operation: OrderOperation, operation_number: int) -> PartOperation:
        part: Part = self.utils.get_plex_material_from_material_op(material_operation)

        # if we dont get a plex op code from this material op then just dont create the routing
        op_id: str = None
        try:
            op_id: str = self._get_op_id_from_material_op(material_operation)
        except CancelledIntegrationActionException:
            return None
        if op_id is None:
            return None

        return PartOperation(
            partId=part.id,
            operationId=op_id,
            type=self._get_type(material_operation),
            operationNumber=operation_number,
            active=True,
            subOperation=False,
            shippable=False
        )

    def to_part_operation(self, plex_part: Part, pp_op: OrderOperation, operation_number: int, is_last_op: bool = False) -> PartOperation:
        return PartOperation(
            partId=plex_part.id,
            operationId=self._get_op_id(pp_op),
            type=self._get_type(pp_op),
            operationNumber=operation_number,
            subOperation=False,
            active=True,
            shippable=is_last_op
        )

    def _get_op_id_from_material_op(self, material_op: OrderOperation) -> str:
        plex_operation_code: str = self.utils.operation_utils.get_variable_value_from_operation(
            material_op,
            self.config.plex_op_code_var
        )

        return self.operations_mapping.get_plex_operation_id_from_plex_op_code(plex_operation_code)

    def _get_op_id(self, pp_op: OrderOperation):
        # get the plex op code by first looking for p3l var, and if not found use the mapping table
        plex_op_code = self.utils.get_plex_operation_code_from_paperless_operation(pp_op, self.operations_mapping)
        # get the plex op id associated with the plex op code
        return self.operations_mapping.get_plex_operation_id_from_plex_op_code(plex_op_code)

    def _get_type(self, operation: OrderOperation):
        """
        tries to get type from operation, defaults to configured value
        """
        return self.utils.operation_utils.get_variable_value_from_operation(
            operation=operation,
            variable_name=self.config.part_operation_type_var_name,
            default=self.config.default_part_operation_type
        )

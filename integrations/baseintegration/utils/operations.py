from paperless.objects.orders import OrderComponent, OrderOperation, OrderCostingVariable
from paperless.objects.quotes import QuoteComponent, QuoteOperation, CostingVariablePayload
from typing import Union
from ...baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


# we need some sort of default so we can easily check if the caller of these functions supplied a default
# previously used None, but None should be allowed to be used as a default
DEFAULT_VAR_VALUE = 'DEFAULT_VAR_VAL'


class OperationUtils:

    def get_operation_variable_value_from_component(self, component: Union[OrderComponent, QuoteComponent], operation_name: str, variable_name: str, default=DEFAULT_VAR_VALUE) -> (str, int, float):
        """
        locate the desired operation
        if not found and it is required throw an exception
        if not found and it is not required then return the default
        """

        # 1) find the operation
        # if none and no default, throw error
        # if none and default, return the default
        # if there is an operation then continue

        # 2) find the value
        # if none and no default throw error
        # if none and default then return default
        # if something return the something

        # 1) find the operation if exists
        operation = None
        ops = component.shop_operations + component.material_operations
        for op in ops:
            if op.operation_definition_name == operation_name:
                # we need to handle the case where this operation exists in the routing twice
                # in this case we will throw an exception, indicating that this function should not be used in that case
                if operation is not None:
                    raise CancelledIntegrationActionException(f'The operation {operation.name} exists in the routing for component {component.part_number} more than once. This function should not be used in this case. Please contact support.')
                operation = op

        # 1a) handle if we don't find the op we're looking for
        if operation is None:
            if default == DEFAULT_VAR_VALUE:
                raise CancelledIntegrationActionException(
                    f'Cannot find operation "{operation_name}" for part {component.part_number}')
            return default

        # 2) get the value we're looking for if it's there
        value = operation.get_variable(variable_name)

        # 2a) handle if there is no value (None)
        if value is None or value == '':
            if default == DEFAULT_VAR_VALUE:
                raise CancelledIntegrationActionException(
                    f'Did not get a value for variable "{variable_name}" in operation "{operation_name}" for part {component.part_number}')
            return default

        return value

    def get_variable_value_from_operation(self, operation: Union[OrderOperation, QuoteOperation], variable_name: str, default=DEFAULT_VAR_VALUE) -> (str, int, float):
        # 1) get the value we're looking for if it's there
        value = operation.get_variable(variable_name)

        # 2) handle if there is no value (None)
        if value is None or value == '':
            if default == DEFAULT_VAR_VALUE:
                raise CancelledIntegrationActionException(
                    f'No value for variable "{variable_name}" in operation "{operation.operation_definition_name}"')
            return default

        return value

    @classmethod
    def get_variable_obj(cls, operation: Union[OrderOperation, QuoteOperation], variable_name: str,
                         qty: int = None) -> Union[OrderCostingVariable, CostingVariablePayload, None]:
        if isinstance(operation, OrderOperation):
            return operation.get_variable_obj(variable_name)
        elif isinstance(operation, QuoteOperation):
            if qty is None:
                return operation.get_variable_for_qty(variable_name, operation.quantities[-1].quantity)
            return operation.get_variable_for_qty(variable_name, qty)

from typing import List, Type
from unittest.mock import patch

from dynamics.objects.base import BaseObject
from paperless.objects.quotes import QuoteCostingVariable, CostingVariablePayload, QuoteComponent


class DynamicsMock:
    def __init__(self, obj_type, method, return_val=None, exception=None):
        self.obj_type = obj_type
        self.method = method
        self.return_val = return_val
        self.exception = exception

    def get_obj(self):
        return patch.object(self.obj_type, self.method,
                            return_value=self.return_val, side_effect=self.exception)


def with_mocks(callback, mocks: List[DynamicsMock], mock_calls={}, counter=0):
    """
    Executes the given callback function, using the given mocks.
    """
    if len(mocks) == 0:
        def get_args(mock, arg_pos=0, call_num=0):
            return mock_calls[mock].call_args_list[call_num][0][arg_pos]
        callback(mock_calls, get_args)
    else:
        new_mocks = mocks.copy()
        mock = new_mocks.pop(0)
        with mock.get_obj() as val:
            new_mock_calls = {
                **mock_calls,
                (mock.obj_type, mock.method): val
            }
            with_mocks(callback, new_mocks, new_mock_calls, counter + 1)


def object_mocks(obj: Type[BaseObject], val):
    """
    Returns mocks for each of the request functions available on the given Dynamics object class.
    """
    return [
        DynamicsMock(obj, 'get_with_filter_strings', return_val=[val]),
        DynamicsMock(obj, 'create', return_val=val),
        DynamicsMock(obj, 'update', return_val=val)
    ]


def get_object_mocks(mock_vals: dict):
    """
    Given a mapping from Dynamics object classes to mock return values, return mocks for each function of each class.
    """
    all_mocks = []
    for obj, mock_val in mock_vals.items():
        all_mocks.extend(object_mocks(obj, mock_val))
    return all_mocks


def add_costing_var(quote_component: QuoteComponent, config_var_name: str, value, processor, material=False):
    label = getattr(processor._exporter.erp_config, config_var_name)

    if isinstance(label, list):
        label = label[0]

    costing_var = QuoteCostingVariable(
        label=label,
        quantities={
            quote_component.quantities[0].quantity: CostingVariablePayload(
                value=value,
                options=None,
                row=value
            )
        },
        quantity_specific=True,
        value=value,
        value_type="",
        variable_class=""
    )

    operations = quote_component.material_operations if material else quote_component.shop_operations
    operations[0].costing_variables.append(costing_var)

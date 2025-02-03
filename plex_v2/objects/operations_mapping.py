from typing import List
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from paperless.objects.orders import OrderOperation


class OperationMapping:
    """
    represents single row in Operations_Mapping custom table
    """

    pp_op_name: str
    plex_op_code: str
    plex_approved_workcenters: List[str]
    plex_approved_suppliers: List[str]
    paperless_only: bool
    plex_operation_id: str

    def __init__(self, pp_op_name: str, plex_op_code: str, plex_approved_workcenters: List[str], plex_approved_suppliers: List[str], paperless_only: bool, plex_op_id: str):
        self.pp_op_name = pp_op_name
        self.plex_op_code = plex_op_code
        self.plex_approved_workcenters = plex_approved_workcenters
        self.plex_approved_suppliers = plex_approved_suppliers
        self.paperless_only = paperless_only
        self.plex_operation_id = plex_op_id


class OperationsMapping:
    """
    representd all rows in the Operations_Mapping custom table
    """

    mappings: List[OperationMapping]

    def __init__(self, operation_mappings: List[OperationMapping]):
        self.mappings = operation_mappings

    def get_approved_workcenter_codes_by_pp_op(self, pp_op: OrderOperation) -> List[str]:
        op_mapping: OperationMapping
        for op_mapping in self.mappings:
            if op_mapping.pp_op_name == pp_op.operation_definition_name:
                return op_mapping.plex_approved_workcenters

        return []

    def get_approved_supplier_codes_by_pp_op(self, pp_op: OrderOperation) -> List[str]:
        op_mapping: OperationMapping
        for op_mapping in self.mappings:
            if op_mapping.pp_op_name == pp_op.operation_definition_name:
                return op_mapping.plex_approved_suppliers

        return []

    def get_approved_supplier_codes_by_plex_op_code(self, plex_op_code: str) -> List[str]:
        op_mapping: OperationMapping
        for op_mapping in self.mappings:
            if op_mapping.plex_op_code == plex_op_code:
                return op_mapping.plex_approved_suppliers

        return []

    def get_plex_op_code_from_op_id(self, op_id: str) -> str:
        op_mapping: OperationMapping
        for op_mapping in self.mappings:
            if op_mapping.plex_operation_id == op_id:
                return op_mapping.plex_op_code

        raise CancelledIntegrationActionException(f'Could not find Plex op code for Plex operation id "{op_id}". '
                                                  f'Please ensure the Operations_Mapping table exists and the '
                                                  f'corresponding operation exists in plex"')

    def get_plex_op_code_from_pp_op_using_mapping_table(self, pp_op: OrderOperation) -> str:
        op_mapping: OperationMapping
        for op_mapping in self.mappings:
            if op_mapping.pp_op_name == pp_op.operation_definition_name:
                return op_mapping.plex_op_code

        raise CancelledIntegrationActionException(f'Could not find Plex op code for Paperless operation "{pp_op.operation_definition_name}". '
                                                  f'Please ensure the Operations_Mapping table exists and the '
                                                  f'corresponding operation exists in plex"')

    def get_plex_op_code_from_pp_op_name(self, pp_op_name: str) -> str:
        op_mapping: OperationMapping
        for op_mapping in self.mappings:
            if op_mapping.pp_op_name == pp_op_name:
                return op_mapping.plex_op_code

        raise CancelledIntegrationActionException(f'Could not find Plex op code for Paperless operation "{pp_op_name}". '
                                                  f'Please ensure the Operations_Mapping table exists and the '
                                                  f'corresponding operation exists in plex"')

    def get_plex_operation_id_from_paperless_operation(self, paperless_op: OrderOperation) -> str:
        op_name = paperless_op.operation_definition_name

        mapping: OperationMapping
        for mapping in self.mappings:
            if mapping.pp_op_name == op_name and mapping.plex_operation_id is not None:
                return mapping.plex_operation_id

        raise CancelledIntegrationActionException(f'Could not find Plex op id for Paperless operation "{op_name}". '
                                                  f'Please ensure the Operations_Mapping table exists and the '
                                                  f'corresponding operation exists in plex"')

    def get_plex_operation_id_from_plex_op_code(self, plex_op_code: str) -> str:
        mapping: OperationMapping
        for mapping in self.mappings:
            if mapping.plex_op_code == plex_op_code:
                return mapping.plex_operation_id

        raise CancelledIntegrationActionException(f'Could not find Plex op id for Plex op code "{plex_op_code}". '
                                                  f'Please ensure the Operations_Mapping table exists and the '
                                                  f'corresponding operation exists in plex"')

    def get_plex_operation_id_from_pp_op_name(self, pp_op_name: str) -> str:
        mapping: OperationMapping
        for mapping in self.mappings:
            if mapping.pp_op_name == pp_op_name:
                return mapping.plex_operation_id

        raise CancelledIntegrationActionException(f'Could not find Plex op id for Paperless operation "{pp_op_name}". '
                                                  f'Please ensure the Operations_Mapping table exists and the '
                                                  f'corresponding operation exists in plex"')

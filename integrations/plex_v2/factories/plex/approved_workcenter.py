from plex_v2.factories.base import BaseFactory
from paperless.objects.orders import OrderOperation
from plex_v2.objects.work_center_export import ApprovedWorkcenterAddUpdate
from plex_v2.objects.part import Part
from plex_v2.objects.operations_mapping import OperationsMapping
from typing import List, Union


class ApprovedWorkCenterFactory(BaseFactory):

    def to_approved_workcenters(self, pp_operation: OrderOperation, plex_part: Part, operations_mapping: OperationsMapping, op_no: int) -> List[ApprovedWorkcenterAddUpdate]:
        """
        returns the plex approved workcenters in the Operations Mapping for the given operation
        """
        approved_workcenters: List[ApprovedWorkcenterAddUpdate] = []

        # 1) get the associated plex operation
        plex_op_code: str = self.utils.get_plex_operation_code_from_paperless_operation(pp_operation, operations_mapping)

        # 2) get the associated approved workcenter codes for this operation
        approved_workcenter_codes_for_op = operations_mapping.get_approved_workcenter_codes_by_pp_op(pp_operation)

        # 3) iterate approved workcenter codes for op and create for each one
        sort_order = self.config.part_operation_increment_step
        approved_workcenter_code: str
        for approved_workcenter_code in approved_workcenter_codes_for_op:

            approved_workcenter = ApprovedWorkcenterAddUpdate(
                Active=True,
                Operation_Code=plex_op_code,
                Operation_No=op_no,
                Part_No=plex_part.number,
                Revision=plex_part.revision,
                Sort_Order=sort_order,
                Workcenter_Code=approved_workcenter_code,
                Setup_Time=self._get_setup_time(pp_operation),
                Standard_Production_Rate=self._get_standard_production_rate(pp_operation),
                Crew_Size=self._get_crew_size(pp_operation)
            )

            approved_workcenters.append(approved_workcenter)

            sort_order += self.config.part_operation_increment_step

        return approved_workcenters

    def _get_op_notes(self, pp_operation: OrderOperation) -> str:
        if pp_operation.notes is None:
            return ''
        return pp_operation.notes

    def _get_setup_time(self, pp_op: OrderOperation) -> Union[int, float]:
        return pp_op.setup_time

    def _get_standard_production_rate(self, pp_op: OrderOperation) -> Union[int, float]:
        if pp_op.runtime is None:
            return float(0)
        return float(1 / pp_op.runtime if pp_op.runtime != 0 else 0)

    def _get_crew_size(self, pp_op: OrderOperation) -> int:
        return self.utils.operation_utils.get_variable_value_from_operation(
            pp_op,
            self.config.crew_size_var,
            self.config.default_approved_workcenter_crew_size
        )

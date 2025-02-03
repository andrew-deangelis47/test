from typing import List, Dict, Union
import math

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import safe_get, safe_get_non_null
from baseintegration.utils.repeat_work_objects import Operation, CostingVariable
from e2.models import (
    OrderRouting,
    Routing,
    Workcntr, OrderDet
)
from e2.importer.utils import (
    RepeatPartUtilObject,
    JobMOMUtil,
    ORDER_ROUTING_COSTING_VARIABLES,
    ROUTING_TO_ORDER_ROUTING_COSTING_VARIABLES,
    WORK_CENTER_COSTING_VARIABLES
)


class OperationProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util: RepeatPartUtilObject) -> RepeatPartUtilObject:
        logger.info(f"Calculating operations on methods of manufacture for repeat work part from E2 with part number {repeat_part_util.e2_part.partno}")
        self.source_database = self._importer.source_database
        self.repeat_part_util = repeat_part_util

        for job_mom_util in repeat_part_util.job_mom_utils:
            if job_mom_util.order_detail:
                job_mom_util.method_of_manufacture.operations = self.get_job_mom_operations(job_mom_util)
                logger.info(f"Calculated operations for job MoM with job number {job_mom_util.order_detail.job_no}")
            else:
                logger.info(f"Not calculating job MoM operations for part number "
                            f"{self.repeat_part_util.repeat_part.part_number} with header {job_mom_util.erp_code} "
                            f"since it is a job req")

        # we do not add operations for imported quotes

        template_operations = self.get_template_mom_operations()
        for template_mom_util in repeat_part_util.template_mom_utils:
            template_mom_util.method_of_manufacture.operations = template_operations
            logger.info(f"Calculated operations for template MoM with part number {template_mom_util.template.partno}")

        return repeat_part_util

    def get_job_mom_operations(self, job_mom_util: JobMOMUtil) -> List[Operation]:
        """
        - Iterates through the OrderRouting objects for this job requirement
        - Creates an Operation on the job method of manufacture for each OrderRouting object
        - Returns the complete list of Operations for this job requirement method of manufacture
        """

        logger.info(f"Calculating operations on a job method of manufacture for repeat work part from E2 with part number {self.repeat_part_util.repeat_part.part_number}")

        operations_list: List[Operation] = []
        order_det: OrderDet = job_mom_util.order_detail
        order_routings: List[OrderRouting] = OrderRouting.objects.using(self.source_database).filter(order_no=order_det.orderno, part_no=order_det.part_no, job_no=order_det.job_no)

        for order_routing in order_routings:
            operation = Operation(
                is_finish=False,
                is_outside_service=bool(safe_get_non_null(order_routing, "work_or_vend", False)),
                name=safe_get_non_null(order_routing, "work_cntr", "WORK CENTER"),
                notes=self.get_order_routing_notes(order_routing),
                position=safe_get_non_null(order_routing, "step_no", 10),
                runtime=self.get_order_routing_cycle_time_hours(order_routing),
                setup_time=self.get_order_routing_setup_time_hours(order_routing),
                total_cost=self.get_order_routing_total_cost(order_routing),
                costing_variables=self.get_order_routing_operation_costing_variables(order_routing)
            )
            operations_list.append(operation)

        return operations_list

    def get_template_mom_operations(self,) -> List[Operation]:
        """
        - Iterates through the Routing objects for this part
        - Creates an Operation on the template method of manufacture for each Routing object
        - Returns the complete list of Operations for this template method of manufacture
        """
        part_number = self.repeat_part_util.e2_part.partno

        logger.info(f"Calculating operations on a template method of manufacture for repeat work part from E2 with part number {part_number}")

        operations_list: List[Operation] = []
        routings: List[Routing] = Routing.objects.using(self.source_database).filter(partno=part_number)

        for routing in routings:
            operation = Operation(
                is_finish=False,
                is_outside_service=bool(safe_get_non_null(routing, "workorvend", False)),
                name=safe_get_non_null(routing, "workcntr", "WORK CENTER"),
                notes=self.get_routing_notes(routing),
                position=safe_get_non_null(routing, "stepno", 10),
                runtime=self.get_routing_cycle_time_hours(routing),
                setup_time=self.get_routing_setup_time_hours(routing),
                total_cost=self.get_routing_total_cost(routing),
                costing_variables=self.get_routing_operation_costing_variables(routing)
            )
            operations_list.append(operation)

        return operations_list

    def get_order_routing_notes(self, order_routing: OrderRouting) -> str:
        notes = ""
        if safe_get(order_routing, "descrip", False):
            notes += f"Description: {order_routing.descrip}\n"
        if safe_get(order_routing, "work_cntr", False):
            notes += f"Work Center: {order_routing.work_cntr}\n"
        if safe_get(order_routing, "status", False):
            notes += f"Status: {order_routing.status}\n"
        return notes

    def get_routing_notes(self, routing: Routing) -> str:
        notes = ""
        if safe_get(routing, "descrip", False):
            notes += f"Description: {routing.descrip}\n"
        if safe_get(routing, "workcntr", False):
            notes += f"Work Center: {routing.workcntr}\n"
        return notes

    def get_order_routing_total_cost(self, order_routing: OrderRouting) -> float:
        requested_qty: int = safe_get_non_null(order_routing, "estim_qty", 1)
        scrap_pct: float = safe_get_non_null(order_routing, "scrap_pct", 0)
        make_qty: int = math.ceil(requested_qty / (1 - scrap_pct))

        setup_time: float = self.get_order_routing_setup_time_hours(order_routing)
        labor_rate: float = safe_get_non_null(order_routing, "labor_rate", 0)
        team_size: int = safe_get_non_null(order_routing, "team_size", 1)
        num_mach_for_job: float = safe_get_non_null(order_routing, "num_mach_for_job", 1)
        cycle_time: float = self.get_order_routing_cycle_time_hours(order_routing)
        pct_eff: float = safe_get_non_null(order_routing, "pct_eff", 1)
        mach_run: float = safe_get_non_null(order_routing, "mach_run", 1)
        labor_setup_cost: float = setup_time * labor_rate * team_size * num_mach_for_job
        labor_run_cost: float = (cycle_time * labor_rate * team_size * make_qty) / (pct_eff * mach_run) if pct_eff * mach_run != 0 else 0
        labor_cost: float = labor_setup_cost + labor_run_cost

        burden_rate: float = safe_get_non_null(order_routing, "burden_rate", 0)
        burden_setup_cost: float = burden_rate * setup_time * num_mach_for_job
        burden_run_cost: float = (burden_rate * make_qty * cycle_time) / pct_eff if pct_eff != 0 else 0
        burden_cost: float = burden_setup_cost + burden_run_cost

        total_cost: float = labor_cost + burden_cost
        return total_cost

    def get_routing_total_cost(self, routing: Routing) -> float:
        requested_qty: int = safe_get_non_null(routing, "estimqty", 1)
        scrap_pct: float = safe_get_non_null(routing, "scrappct", 0)
        make_qty: int = math.ceil(requested_qty / (1 - scrap_pct))

        setup_time: float = self.get_routing_setup_time_hours(routing)
        labor_rate: float = safe_get_non_null(routing, "laborrate", 0)
        team_size: int = safe_get_non_null(routing, "teamsize", 1)
        num_mach_for_job: float = safe_get_non_null(routing, "nummachforjob", 1)
        cycle_time: float = self.get_routing_cycle_time_hours(routing)
        pct_eff: float = safe_get_non_null(routing, "pcteff", 1)
        mach_run: float = safe_get_non_null(routing, "machrun", 1)
        labor_setup_cost: float = setup_time * labor_rate * team_size * num_mach_for_job
        labor_run_cost: float = (cycle_time * labor_rate * team_size * make_qty) / (pct_eff * mach_run) if pct_eff * mach_run != 0 else 0
        labor_cost: float = labor_setup_cost + labor_run_cost

        burden_rate: float = safe_get_non_null(routing, "burdenrate", 0)
        burden_setup_cost: float = burden_rate * setup_time * num_mach_for_job
        burden_run_cost: float = (burden_rate * make_qty * cycle_time) / pct_eff if pct_eff != 0 else 0
        burden_cost: float = burden_setup_cost + burden_run_cost

        total_cost: float = labor_cost + burden_cost
        return total_cost

    def get_order_routing_operation_costing_variables(self, order_routing: OrderRouting) -> List[CostingVariable]:
        costing_variables: List[CostingVariable] = []
        self.add_order_routing_costing_variables(costing_variables, order_routing)
        self.add_work_center_costing_variables(costing_variables, order_routing)
        return costing_variables

    def add_order_routing_costing_variables(self, costing_variables: List[CostingVariable], order_routing: OrderRouting):
        self.add_object_costing_variables(costing_variables, ORDER_ROUTING_COSTING_VARIABLES.items(), order_routing)

    def get_routing_operation_costing_variables(self, routing: Routing) -> List[CostingVariable]:
        costing_variables: List[CostingVariable] = []
        self.add_routing_costing_variables(costing_variables, routing)
        self.add_work_center_costing_variables(costing_variables, routing)
        return costing_variables

    def add_routing_costing_variables(self, costing_variables: List[CostingVariable], routing: Routing):
        for routing_name, order_routing_name in ROUTING_TO_ORDER_ROUTING_COSTING_VARIABLES.items():
            costing_variable_value = safe_get_non_null(routing, routing_name, ORDER_ROUTING_COSTING_VARIABLES[order_routing_name])
            costing_variable = CostingVariable(
                label=order_routing_name,
                value=costing_variable_value
            )
            costing_variables.append(costing_variable)

    def add_work_center_costing_variables(self, costing_variables: List[CostingVariable], routing: Union[OrderRouting, Routing]):
        work_centers: List[Workcntr] = []
        if isinstance(routing, OrderRouting):
            work_centers = Workcntr.objects.using(self.source_database).filter(oldworkcntr=routing.work_cntr)
        else:
            work_centers = Workcntr.objects.using(self.source_database).filter(oldworkcntr=routing.workcntr)

        for work_center in work_centers:
            self.add_object_costing_variables(costing_variables, WORK_CENTER_COSTING_VARIABLES.items(), work_center)

    def add_object_costing_variables(self, costing_variables: List[CostingVariable], costing_variables_dict: Dict, object: Union[OrderRouting, Routing, Workcntr]):
        for variable_name, default_value in costing_variables_dict:
            costing_variable_value = safe_get_non_null(object, variable_name, default_value)
            costing_variable = CostingVariable(
                label=variable_name,
                value=costing_variable_value
            )
            costing_variables.append(costing_variable)

    def get_routing_setup_time_hours(self, routing: Routing) -> float:
        setup_time: float = safe_get_non_null(routing, "setuptime", 0)
        time_unit = safe_get_non_null(routing, "timeunit")
        return self.to_hours(setup_time, time_unit)

    def get_routing_cycle_time_hours(self, routing: Routing) -> float:
        cycle_time: float = safe_get_non_null(routing, "cycletime", 0)
        time_unit = safe_get_non_null(routing, "cycleunit")
        return self.to_hours(cycle_time, time_unit)

    def get_order_routing_setup_time_hours(self, order_routing: OrderRouting):
        setup_time: float = safe_get_non_null(order_routing, "setup_time", 0)
        time_unit = safe_get_non_null(order_routing, "time_unit")
        return self.to_hours(setup_time, time_unit)

    def get_order_routing_cycle_time_hours(self, order_routing: OrderRouting):
        cycle_time: float = safe_get_non_null(order_routing, "cycle_time", 0)
        time_unit = safe_get_non_null(order_routing, "cycle_unit")
        return self.to_hours(cycle_time, time_unit)

    def to_hours(self, time: float, time_unit: str):
        if time_unit == 'M':
            time /= 60
        elif time_unit == 'S':
            time /= (60 * 60)
        return time

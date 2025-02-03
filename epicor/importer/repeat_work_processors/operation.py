from baseintegration.importer.import_processor import BaseImportProcessor
from epicor.quote import QuoteOperation, QuoteDetail, QuoteAssembly
from epicor.job import JobOperation, JobEntry, JobAssembly
from epicor.engineering_workbench import EWBRev, EWBOperation
from epicor.importer.utils import RepeatPartUtilObject, QuoteMOMUtil, JobMOMUtil, JOB_OPERATION_COSTING_VARS, \
    QUOTE_OPERATION_COSTING_VARS, EWBMOMUtil
from typing import List, Union
from baseintegration.utils.repeat_work_objects import Operation, CostingVariable
from baseintegration.utils import logger, safe_get
from decimal import Decimal
from epicor.importer.epicor_client_cache import EpicorClientCache


class OperationProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util_object: RepeatPartUtilObject, epicor_client_cache: EpicorClientCache,
                 bulk=False):
        logger.info("OperationProcessor - Attempting to create Operations")
        self.bulk = bulk
        if epicor_client_cache:
            self.epicor_client_cache: EpicorClientCache = epicor_client_cache
        else:
            self.epicor_client_cache: EpicorClientCache = repeat_part_util_object.epicor_client_cache

        for quote_mom_util in repeat_part_util_object.quote_mom_utils:
            quote_mom_util: QuoteMOMUtil = quote_mom_util
            quote_mom_util.mom.operations = self._get_quote_mom_shop_operations(quote_mom_util)

        for job_mom_util in repeat_part_util_object.job_mom_utils:
            job_mom_util: JobMOMUtil = job_mom_util
            job_mom_util.mom.operations = self._get_job_mom_shop_operations(job_mom_util)

        for ewb_mom_util in repeat_part_util_object.ewb_mom_utils:
            ewb_mom_util: EWBMOMUtil = ewb_mom_util
            ewb_mom_util.mom.operations = self._get_ewb_mom_shop_operations(
                ewb_mom_util, repeat_part_util_object.repeat_part.part_number)

        return repeat_part_util_object

    def _get_quote_mom_shop_operations(self, quote_mom_util: QuoteMOMUtil) -> List[Operation]:
        operations_list: List[Operation] = []
        epicor_quote_detail: QuoteDetail = quote_mom_util.epicor_quote_detail
        epicor_quote_assembly: QuoteAssembly = quote_mom_util.quote_assembly

        # Get job operations from the epicor client cache
        epicor_operations: List[QuoteOperation] = self.get_quote_operations_from_epicor_client_cache(
            epicor_quote_detail.QuoteNum, epicor_quote_detail.QuoteLine, epicor_quote_assembly.AssemblySeq
        )

        for epicor_operation in epicor_operations:
            if (epicor_quote_detail.QuoteNum == epicor_operation.QuoteNum) and (
                    epicor_quote_detail.QuoteLine == epicor_operation.QuoteLine) and (
                    epicor_quote_assembly.AssemblySeq == epicor_operation.AssemblySeq
            ):
                operation_total_cost = self.get_quote_operation_total_cost(quote_mom_util, epicor_operation)
                is_outside_service = bool(epicor_operation.SubContract)
                if is_outside_service:
                    operation_total_cost = safe_get(epicor_operation, "EstUnitCost", 0)

                operation = Operation(
                    is_finish=False,  # No concept of a finish in Epicor
                    is_outside_service=is_outside_service,
                    name=str(epicor_operation.OpCode),
                    notes=self._get_operation_notes(epicor_operation),
                    position=int(epicor_operation.OprSeq),
                    runtime=self._get_operation_runtime(epicor_operation),
                    setup_time=float(epicor_operation.HoursPerMachine),
                    total_cost=operation_total_cost,
                    costing_variables=self._get_costing_variables(epicor_operation),
                )
                operations_list.append(operation)

        return operations_list

    def _get_job_mom_shop_operations(self, job_mom_util: JobMOMUtil) -> List[Operation]:
        operations_list: List[Operation] = []
        epicor_job_entry: JobEntry = job_mom_util.epicor_job
        epicor_job_assembly: JobAssembly = job_mom_util.job_assembly

        epicor_operations: List[JobOperation] = self.get_job_operations_from_epicor_client_cache(
            epicor_job_entry.JobNum, epicor_job_assembly.AssemblySeq
        )

        for epicor_operation in epicor_operations:
            if (epicor_job_entry.JobNum == epicor_operation.JobNum) and (
                    epicor_job_assembly.AssemblySeq == epicor_operation.AssemblySeq
            ):

                total_cost = safe_get(epicor_operation, "EstBurdenCost", 0) + safe_get(
                    epicor_operation, "EstLaborCost", 0)
                is_outside_service = bool(epicor_operation.SubContract)
                if is_outside_service:
                    total_cost = safe_get(epicor_operation, "EstSubCost", 0)

                operation = Operation(
                    is_finish=False,  # No concept of a finish in Epicor
                    is_outside_service=is_outside_service,
                    name=str(epicor_operation.OpCode),
                    notes=self._get_operation_notes(epicor_operation),
                    position=int(epicor_operation.OprSeq),
                    runtime=self._get_operation_runtime(epicor_operation),
                    setup_time=float(epicor_operation.EstSetHours),
                    total_cost=total_cost,
                    costing_variables=self._get_costing_variables(epicor_operation),
                )
                operations_list.append(operation)

        return operations_list

    def _get_ewb_mom_shop_operations(self, ewb_mom_util: EWBMOMUtil, part_number: str) -> List[Operation]:
        operations_list: list = []
        epicor_ewb_rev: EWBRev = ewb_mom_util.epicor_ewb_rev

        epicor_operations: List[EWBOperation] = self.get_ewb_operations_from_epicor_client_cache(
            epicor_ewb_rev.SysRowID, part_number
        )

        for epicor_operation in epicor_operations:
            operation = Operation(
                is_finish=False,  # No concept of a finish in Epicor
                is_outside_service=bool(epicor_operation.SubContract),
                name=str(epicor_operation.OpCode),
                notes=self._get_operation_notes(epicor_operation),
                position=int(epicor_operation.OprSeq),
                runtime=self._get_operation_runtime(epicor_operation),
                setup_time=float(epicor_operation.EstSetHours),
                total_cost=0,  # TODO: add total cost value
                costing_variables=self._get_costing_variables(epicor_operation),
            )
            operations_list.append(operation)

        return operations_list

    def _get_costing_variables(self, epicor_operation: Union[JobOperation, QuoteOperation, EWBOperation]) -> List[CostingVariable]:
        costing_variables: list = []
        costing_vars_dict = JOB_OPERATION_COSTING_VARS.items()
        if isinstance(epicor_operation, QuoteOperation):
            costing_vars_dict = QUOTE_OPERATION_COSTING_VARS.items()

        for variable_name, default_val in costing_vars_dict:
            epicor_value = safe_get(epicor_operation, variable_name, default_val)
            if isinstance(epicor_value, (int, float, Decimal)):
                epicor_value = float(epicor_value)
            elif isinstance(epicor_value, bool):
                epicor_value = bool(epicor_value)
            else:
                epicor_value = str(epicor_value)

            costing_var = CostingVariable(
                label=variable_name,
                value=epicor_value
            )
            costing_variables.append(costing_var)

        return costing_variables

    def _get_operation_runtime(self, epicor_operation: Union[JobOperation, QuoteOperation, EWBOperation]) -> float:
        if isinstance(epicor_operation, JobOperation):
            unadjusted_runtime = safe_get(epicor_operation, "EstProdHours", 0)
        else:
            unadjusted_runtime = safe_get(epicor_operation, "ProdStandard", 0)
        runtime_units = str(epicor_operation.StdFormat)

        runtime = 0
        if unadjusted_runtime > 0:
            runtime_conversion_calc_dict: dict = {
                "HP": unadjusted_runtime,  # Hrs/Part (standard Paperless runtime units)
                "PH": 1 / unadjusted_runtime,  # Parts/Hr (rounded down to int)
                "PM": (1 / unadjusted_runtime) / 60,  # Parts/Min (rounded down to int)
                "MP": unadjusted_runtime / 60,  # min / piece
                "HR": unadjusted_runtime  # TODO: How do we want to handle fixed hours as a runtime from Epicor?
            }
            runtime = runtime_conversion_calc_dict.get(runtime_units)

        return float(runtime)

    def _get_operation_notes(self, epicor_operation: Union[JobOperation, QuoteOperation, EWBOperation]):
        notes = ''
        if safe_get(epicor_operation, 'Description', False):
            notes += f"Description: {epicor_operation.Description}\n"
        if safe_get(epicor_operation, "CommentText", False):
            notes += f"CommentText: {epicor_operation.CommentText}\n"
        return notes

    def get_quote_operations_from_epicor_client_cache(self, quote_num: str, quote_line: str, assembly_seq: int
                                                      ) -> List[QuoteOperation]:
        quote_operations_list: List[QuoteOperation] = []
        for quote_assembly in self.epicor_client_cache.nested_quote_assembly_cache:
            if (quote_assembly.QuoteNum == quote_num) and (quote_assembly.QuoteLine == quote_line) and (
                    quote_assembly.AssemblySeq == assembly_seq):
                quote_operations_list = quote_assembly.QuoteOprs

        return quote_operations_list

    def get_job_operations_from_epicor_client_cache(self, job_num: str, assembly_seq: int) -> List[JobOperation]:
        job_operations_list: List[JobOperation] = []
        for job_entry in self.epicor_client_cache.nested_job_entry_cache:
            if job_entry.JobNum == job_num:
                for job_assembly in job_entry.JobAsmbls:
                    if job_assembly.AssemblySeq == assembly_seq:
                        job_operations_list = job_assembly.JobOpers

        return job_operations_list

    def get_ewb_operations_from_epicor_client_cache(self, sys_row_id: str, part_number: str) -> List[EWBOperation]:
        ewb_operations_list: List[EWBOperation] = []
        for ewb_rev in self.epicor_client_cache.nested_ewb_rev_cache:
            if ewb_rev.SysRowID == sys_row_id:
                for ewb_operation in ewb_rev.ECOOprs:
                    if ewb_operation.PartNum == part_number:
                        ewb_operations_list.append(ewb_operation)

        return ewb_operations_list

    def get_quote_operation_total_cost(self, quote_mom_util: QuoteMOMUtil, epicor_operation: QuoteOperation):
        quoted_qty = float(safe_get(quote_mom_util.epicor_quote_qty, "OurQuantity", 1))
        # Time fields
        est_setup_hours = float(safe_get(epicor_operation, "EstSetHours", 0))
        prod_standard = float(safe_get(epicor_operation, "ProdStandard", 0))
        # Burden fields:
        setup_burden_rate = float(safe_get(epicor_operation, "SetupBurRate", 0))
        prod_burden_rate = float(safe_get(epicor_operation, "ProdBurRate", 0))
        # Labor fields:
        setup_labor_rate = float(safe_get(epicor_operation, "SetupLabRate", 0))
        prod_labor_rate = float(safe_get(epicor_operation, "ProdLabRate", 0))
        setup_crew_size = float(safe_get(epicor_operation, "SetUpCrewSize", 1))
        prod_crew_size = float(safe_get(epicor_operation, "ProdCrewSize", 1))

        std_basis_dict = {
            "E": 1,  # "Each"
            "C": 100,  # "Per 100's"
            "M": 1000,  # "Per 1000's"
            "T": 10000  # "Per 10000's"
        }
        std_basis = std_basis_dict.get(safe_get(epicor_operation, "StdBasis", "E"), 1)
        std_format = safe_get(epicor_operation, "StdFormat", "HP")

        # Assumes starting units are "HP" (hours/part)
        converted_runtime = prod_standard
        if std_format == "MP":
            converted_runtime = prod_standard / 60
        elif std_format == "PH":
            converted_runtime = 1 / prod_standard if prod_standard > 0 else 0
        elif std_format == "PM":
            converted_runtime = 1 / prod_standard / 60 if prod_standard > 0 else 0
        elif std_format == "HR":
            quoted_qty = 1

        # Quote operation costing formulas:
        burden_total = (est_setup_hours * setup_burden_rate) + (
            (quoted_qty / std_basis) * converted_runtime * prod_burden_rate)
        labor_total = (est_setup_hours * setup_labor_rate * setup_crew_size) + (
            (quoted_qty / std_basis) * converted_runtime * prod_labor_rate * prod_crew_size)
        op_total_cost = labor_total + burden_total
        return round(op_total_cost, 3)

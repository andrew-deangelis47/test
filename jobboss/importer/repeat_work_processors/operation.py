from baseintegration.importer.import_processor import BaseImportProcessor
import jobboss.models as jb
from baseintegration.utils.repeat_work_objects import Operation, CostingVariable
from jobboss.utils.repeat_work_utils import RepeatPartUtilObject, QuoteMOMUtil, JobMOMUtil, \
    SHOP_OP_COSTING_VARS, get_empty_string_if_none
from baseintegration.utils import safe_get, logger
from typing import Union


class OperationProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util_object: RepeatPartUtilObject):
        logger.info("OperationProcessor - Attempting to create Operations")
        self.source_database = self._importer.source_database

        repeat_part = repeat_part_util_object.repeat_part
        if repeat_part is None:
            return None

        for quote_mom_util in repeat_part_util_object.quote_mom_utils:
            quote_mom_util: QuoteMOMUtil = quote_mom_util
            quote_mom_util.mom.operations = []
            self.get_quote_mom_shop_operations(quote_mom_util)
            self.get_mom_operation_totals(quote_mom_util)

        for job_mom_util in repeat_part_util_object.job_mom_utils:
            job_mom_util: JobMOMUtil = job_mom_util
            job_mom_util.mom.operations = []
            self.get_job_mom_shop_operations(job_mom_util)
            self.get_mom_operation_totals(job_mom_util)

        return repeat_part_util_object

    def get_quote_mom_shop_operations(self, quote_mom_util: QuoteMOMUtil):
        jb_quote = quote_mom_util.jb_quote
        logger.info(f"Creating Operations for JobBOSS Quote: {jb_quote.quote}")
        jb_quote_qty = quote_mom_util.jb_quote_qty
        jb_operations = jb.QuoteOperation.objects.using(self.source_database).filter(quote=jb_quote.quote)

        for jb_operation in jb_operations:
            is_outside_service = self.is_outside_service(jb_operation)
            if is_outside_service:
                wc_or_vendor_object = self.get_jb_vendor_object(jb_operation.vendor)
                wc_or_vendor_attr = "vendor"
                wc_or_vendor_costing_var = self.get_vendor_costing_var(jb_operation)
            else:
                wc_or_vendor_object = self.get_jb_work_center_object(jb_operation.work_center)
                wc_or_vendor_attr = "work_center"
                wc_or_vendor_costing_var = self.get_work_center_costing_var(jb_operation)

            if wc_or_vendor_object is not None:
                short_description = get_empty_string_if_none(safe_get(jb_operation, "description", None))
                long_description = get_empty_string_if_none(safe_get(jb_operation, "note_text", None))
                notes_concat = f'{short_description}\n{long_description}' if short_description else long_description
                pp_operation = Operation(
                    is_finish=False,  # No concept of a finish in JB, only inside ops vs. outside ops
                    is_outside_service=is_outside_service,
                    name=safe_get(wc_or_vendor_object, wc_or_vendor_attr, "NO NAME"),
                    notes=notes_concat,
                    position=safe_get(jb_operation, "sequence", 0),
                    runtime=safe_get(jb_operation, "est_run_per_part", 0),  # Hrs/Part
                    setup_time=safe_get(jb_operation, "est_setup_hrs", 0),
                    costing_variables=self.get_shop_operation_costing_variables(jb_operation)
                )
                if pp_operation.runtime == 0:
                    pp_operation.runtime = self.get_runtime_conversion(jb_operation.run, jb_operation.run_method)

                pp_operation.costing_variables.append(wc_or_vendor_costing_var)
                pp_operation.costing_variables.append(self.is_job_costing_var("False"))
                pp_operation.total_cost = self.get_jb_quote_operation_cost(jb_operation, jb_quote_qty)
                quote_mom_util.mom.operations.append(pp_operation)

    def get_job_mom_shop_operations(self, job_mom_util: JobMOMUtil):
        jb_job = job_mom_util.jb_job
        logger.info(f"Creating Operations for JobBOSS Job: {jb_job.job}")
        jb_operations = jb.JobOperation.objects.using(self.source_database).filter(job=jb_job.job)

        for jb_operation in jb_operations:
            is_outside_service = self.is_outside_service(jb_operation)
            if is_outside_service:
                wc_or_vendor_object = self.get_jb_vendor_object(jb_operation.vendor)
                wc_or_vendor_attr = "vendor"
                wc_or_vendor_costing_var = self.get_vendor_costing_var(jb_operation)
            else:
                wc_or_vendor_object = self.get_jb_work_center_object(jb_operation.work_center)
                wc_or_vendor_costing_var = self.get_work_center_costing_var(jb_operation)
                wc_or_vendor_attr = "work_center"

            if wc_or_vendor_object is not None:
                short_description = get_empty_string_if_none(safe_get(jb_operation, "description", None))
                long_description = get_empty_string_if_none(safe_get(jb_operation, "note_text", None))
                notes_concat = f'{short_description}\n{long_description}' if short_description else long_description
                pp_operation = Operation(
                    is_finish=False,  # No concept of a finish in JB, only inside ops vs. outside ops
                    is_outside_service=is_outside_service,
                    name=safe_get(wc_or_vendor_object, wc_or_vendor_attr, "NO NAME"),
                    notes=notes_concat,
                    position=safe_get(jb_operation, "sequence", 0),
                    runtime=safe_get(jb_operation, "est_run_per_part", 0),
                    setup_time=safe_get(jb_operation, "est_setup_hrs", 0),
                    costing_variables=self.get_shop_operation_costing_variables(jb_operation)
                )
                if pp_operation.runtime == 0:
                    pp_operation.runtime = self.get_runtime_conversion(jb_operation.run, jb_operation.run_method)

                pp_operation.costing_variables.append(wc_or_vendor_costing_var)
                pp_operation.costing_variables.append(self.is_job_costing_var("True"))
                pp_operation.total_cost = self.get_jb_job_operation_cost(jb_operation, pp_operation)
                job_mom_util.mom.operations.append(pp_operation)

    def get_shop_operation_costing_variables(self, jb_operation: jb.Operation):
        pp_costing_vars = []
        for pp_var_name, jb_var_tuple in SHOP_OP_COSTING_VARS.items():
            value = safe_get(jb_operation, jb_var_tuple[0], None)
            if value is not None:
                if jb_var_tuple[1] == str:
                    pp_costing_vars.append(
                        CostingVariable(
                            label=pp_var_name,
                            value=str(value)
                        ).to_json()
                    )
                else:
                    pp_costing_vars.append(
                        CostingVariable(
                            label=pp_var_name,
                            value=float(value)
                        ).to_json()
                    )
        return pp_costing_vars

    def get_work_center_costing_var(self, jb_operation: Union[jb.JobOperation, jb.QuoteOperation]):
        if jb_operation.work_center is not None:
            work_center_costing_var = CostingVariable(
                label="work_center",
                value=str(safe_get(jb_operation.work_center, "work_center", "MISSING"))
            ).to_json()
            return work_center_costing_var
        return None

    def get_vendor_costing_var(self, jb_operation: Union[jb.JobOperation, jb.QuoteOperation]):
        if jb_operation.vendor is not None:
            vendor_costing_var = CostingVariable(
                label="vendor",
                value=str(safe_get(jb_operation.vendor, "vendor", "MISSING"))
            ).to_json()
            return vendor_costing_var
        return None

    def is_job_costing_var(self, is_job):
        return CostingVariable(label="is_job", value=is_job).to_json()

    def get_jb_work_center_object(self, jb_work_center: jb.WorkCenter):
        if isinstance(jb_work_center, jb.WorkCenter):
            return jb_work_center
        return None

    def get_jb_vendor_object(self, jb_vendor: jb.Vendor):
        if isinstance(jb_vendor, jb.Vendor):
            return jb_vendor
        return None

    def is_outside_service(self, jb_operation):
        if jb_operation.inside_oper == 1:
            return False
        return True

    def get_jb_quote_operation_cost(self, jb_operation: jb.QuoteOperation, jb_qty: jb.QuoteQty):
        # TODO: Rounding is a little ugly here. Fix it and get more accurate costing.
        make_qty = int(safe_get(jb_qty, "make_quantity", 1))  # Quotes store make qty on operation
        setup_time = float(jb_operation.est_setup_hrs)
        runtime = self.get_runtime_conversion(jb_operation.run, jb_operation.run_method)

        if jb_operation.inside_oper == 0:
            total_cost = make_qty * float(jb_operation.est_unit_cost)
            if total_cost < float(jb_operation.minimum_chg_amt):
                total_cost = float(jb_operation.minimum_chg_amt)
            return total_cost
        else:
            # Convert percentage variables to decimals
            attended_pct_decimal = (float(jb_operation.attended_pct) / 100)
            efficiency_pct_decimal = (float(jb_operation.efficiency_pct) / 100)

            # Calculate labor and burden costs associated with setup time
            setup_labor_cost = setup_time * float(jb_operation.setup_labor_rate)
            setup_burden_cost = (float(jb_operation.setup_labor_burden_rate) + float(jb_operation.machine_burden_rate) + float(jb_operation.ga_burden_rate)) * setup_time

            # Calculate labor and burden costs associated with runtime
            part_quantity = make_qty
            if jb_operation.run_method == "FixedHrs":
                part_quantity = 1

            run_labor_cost = runtime * float(jb_operation.run_labor_rate) * attended_pct_decimal * part_quantity / efficiency_pct_decimal
            run_burden_cost = (float(jb_operation.run_labor_burden_rate) * attended_pct_decimal) + (float(jb_operation.machine_burden_rate) + float(jb_operation.ga_burden_rate)) * part_quantity * runtime / efficiency_pct_decimal

            # Sum labor costs and setup costs
            total_labor_cost = setup_labor_cost + run_labor_cost
            total_burden_cost = setup_burden_cost + run_burden_cost

            return total_labor_cost + total_burden_cost

    def get_runtime_conversion(self, runtime, unit):
        runtime_dict = {
            "Hrs/Part": runtime,
            "Min/Part": runtime / 60,
            "Sec/Part": runtime / 3600,
            "Parts/Hr": 1 / runtime if runtime > 0 else 0,
            "Parts/Min": (1 / runtime if runtime > 0 else 0) * 60,
            "Parts/Sec": (1 / runtime if runtime > 0 else 0) * 3600,
            "FixedHrs": runtime
        }
        return runtime_dict.get(unit, 0)

    def get_jb_job_operation_cost(self, jb_operation: jb.JobOperation, pp_operation: Operation):
        # JB Job outside operations store the operation total cost
        if pp_operation.is_outside_service:
            return float(safe_get(jb_operation, "est_total_cost", 0))
        else:
            return float(jb_operation.est_setup_labor + jb_operation.est_run_labor + jb_operation.est_labor_burden + jb_operation.est_machine_burden + jb_operation.est_ga_burden)

    def get_mom_operation_totals(self, mom_util: Union[QuoteMOMUtil, JobMOMUtil]):
        inside_cost = 0
        outside_cost = 0
        for operation in mom_util.operations:
            if operation.is_outside_service:
                outside_cost += operation.total_cost
            else:
                inside_cost += operation.total_cost
        mom_util.mom.inside_processing_total_cost = inside_cost
        mom_util.mom.outside_processing_total_cost = outside_cost

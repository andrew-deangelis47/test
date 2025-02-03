from baseintegration.importer.import_processor import BaseImportProcessor
import jobboss.models as jb
from baseintegration.utils.repeat_work_objects import RequiredMaterials, CostingVariable
from jobboss.utils.repeat_work_utils import RepeatPartUtilObject, QuoteMOMUtil, JobMOMUtil, \
    get_empty_string_if_none, MATERIAL_OP_COSTING_VARS, MATERIAL_MASTER_COSTING_VARS
from baseintegration.utils import safe_get, logger
from typing import Union
from decimal import Decimal
from math import ceil


class RequiredMaterialProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util_object: RepeatPartUtilObject):
        logger.info("RequiredMaterialProcessor - Attempting to create RequiredMaterials")
        self.source_database = self._importer.source_database

        repeat_part = repeat_part_util_object.repeat_part
        if repeat_part is None:
            return None

        for quote_mom_util in repeat_part_util_object.quote_mom_utils:
            quote_mom_util: QuoteMOMUtil = quote_mom_util
            quote_mom_util.mom.required_materials = []
            self.get_quote_mom_material_operations(quote_mom_util)
            self.sum_quote_req_material_costs(quote_mom_util)

        for job_mom_util in repeat_part_util_object.job_mom_utils:
            job_mom_util: JobMOMUtil = job_mom_util
            job_mom_util.mom.required_materials = []
            self.get_job_mom_material_operations(job_mom_util)
            self.sum_job_req_material_costs(job_mom_util)

        return repeat_part_util_object

    def get_quote_mom_material_operations(self, quote_mom_util: QuoteMOMUtil):
        jb_quote = quote_mom_util.jb_quote
        mom_requested_qty = quote_mom_util.mom.requested_qty
        logger.info(f"Creating RequiredMaterials for JobBOSS Quote: {jb_quote.quote}")
        jb_materials = jb.QuoteReq.objects.using(self.source_database).filter(quote=jb_quote.quote, type="R")

        if not jb_materials:
            logger.info(f"No raw stock material found forJobBOSS Quote: {jb_quote.quote}")

        for jb_material in jb_materials:
            total_cost = 0
            material_master_record = jb.Material.objects.using(self.source_database).filter(
                material=jb_material.material).first()
            if jb_material.quantity_per_basis == "B":
                total_cost = self.get_quote_bar_material_operation_total_cost(mom_requested_qty, jb_material, material_master_record)
            elif jb_material.quantity_per_basis == "S":
                total_cost = self.get_quote_sheet_material_operation_total_cost(mom_requested_qty, jb_material, material_master_record)

            pp_material_op = RequiredMaterials(
                name=safe_get(jb_material, "material", "NO NAME"),
                notes=get_empty_string_if_none(safe_get(jb_material, "description", None)),
                total_cost=float(total_cost),
                costing_variables=self.get_material_costing_vars(jb_material)
            )
            vendor = self.get_material_vendor(jb_material)
            if vendor:
                pp_material_op.costing_variables.append(vendor)
            self.add_material_master_costing_vars(pp_material_op, material_master_record)
            quote_mom_util.mom.required_materials.append(pp_material_op)

    def get_job_mom_material_operations(self, job_mom_util: JobMOMUtil):
        jb_job = job_mom_util.jb_job
        logger.info(f"Creating RequiredMaterials for JobBOSS Job: {jb_job.job}")
        jb_materials = jb.MaterialReq.objects.using(self.source_database).filter(job=jb_job.job, type="R")

        for jb_material in jb_materials:
            material_master_record = jb.Material.objects.using(self.source_database).filter(material=jb_material.material).first()

            pp_material_op = RequiredMaterials(
                name=safe_get(jb_material, "material", "NO NAME"),
                notes=get_empty_string_if_none(safe_get(jb_material, "description", None)),
                total_cost=float(safe_get(jb_material, "est_total_cost", 0)),  # JB stores total cost for job material requirements
                costing_variables=self.get_material_costing_vars(jb_material)
            )
            vendor = self.get_material_vendor(jb_material)
            if vendor:
                pp_material_op.costing_variables.append(vendor)
            self.add_material_master_costing_vars(pp_material_op, material_master_record)
            job_mom_util.mom.required_materials.append(pp_material_op)

    def get_material_costing_vars(self, jb_material: Union[jb.MaterialReq, jb.QuoteReq]):
        """
        NOTE:
        - All material requirements must share the same variables. They will all map to the same operation in
        Paperless Parts. Control flow for different JB material calcs is driven by P3L logic.
        - If a JB QuoteReq record contains an attribute that only exists on a MaterialReq, the default from the tuple
        in the util will be assigned.
        """
        pp_costing_vars = []
        for pp_var_name, jb_var_tuple in MATERIAL_OP_COSTING_VARS.items():
            jb_value = safe_get(jb_material, jb_var_tuple[0], None)
            if jb_value is not None:
                value = self.typecast_costing_variable(jb_value)
                costing_var = CostingVariable(
                    label=pp_var_name,
                    value=value
                ).to_json()
                if costing_var:
                    pp_costing_vars.append(costing_var)
        return pp_costing_vars

    def add_material_master_costing_vars(self, pp_material_op, material_master_record):
        if material_master_record:
            for pp_var_name, jb_var_tuple in MATERIAL_MASTER_COSTING_VARS.items():
                jb_value = safe_get(material_master_record, jb_var_tuple[0], None)
                if jb_value is not None:
                    value = self.typecast_costing_variable(jb_value)
                    costing_var = CostingVariable(
                        label=pp_var_name,
                        value=value
                    ).to_json()
                    if costing_var:
                        pp_material_op.costing_variables.append(costing_var)

    def typecast_costing_variable(self, value):
        if type(value) in (str, bool):
            return str(value)
        return float(value)

    def get_material_vendor(self, jb_material: Union[jb.QuoteReq, jb.MaterialReq]):
        if jb_material.vendor is not None:
            vendor_costing_var = CostingVariable(
                label="vendor",
                value=str(safe_get(jb_material.vendor, "vendor", "MISSING"))
            ).to_json()
            if vendor_costing_var:
                return vendor_costing_var
        return None

    def sum_quote_req_material_costs(self, quote_mom_util: QuoteMOMUtil):
        quote_req_cost = 0
        for mat in quote_mom_util.required_materials:
            quote_req_cost += round(float(mat.total_cost), 3)
        quote_mom_util.mom.required_materials_total_cost = quote_req_cost

    def sum_job_req_material_costs(self, job_mom_util: JobMOMUtil):
        material_req_cost = 0
        for mat in job_mom_util.required_materials:
            material_req_cost += round(float(mat.total_cost), 3)
        job_mom_util.mom.required_materials_total_cost = material_req_cost

    def get_quote_bar_material_operation_total_cost(self, mom_requested_qty: int, jb_material: jb.QuoteReq,
                                                    material_master_record: jb.Material) -> Union[int, float, Decimal]:
        bar_length = jb_material.bar_length if jb_material.bar_length > 0 else material_master_record.is_length
        part_length = jb_material.part_length
        bar_end = jb_material.bar_end
        cutoff = jb_material.cutoff
        last_cost = material_master_record.last_cost
        cost_unit_conv = jb_material.cost_unit_conv
        cost_uofm = jb_material.cost_uofm

        parts_per_bar = (bar_length - bar_end) / (part_length + cutoff + jb_material.facing) if part_length > 0 else 0

        if cost_uofm == "lb":
            total_bars_required = ceil(1 / parts_per_bar) if parts_per_bar > 0 else 0
            total_bar_length = total_bars_required / parts_per_bar if parts_per_bar > 0 else 0
            purchase_qty = bar_length * total_bar_length / 12
            required_qty = mom_requested_qty * purchase_qty
            return required_qty * last_cost * cost_unit_conv

        elif cost_uofm == "ea":
            total_bars_required = round(1 / parts_per_bar, 2) if parts_per_bar > 0 else 0
            return total_bars_required * last_cost * mom_requested_qty

        else:
            logger.info("Unsupported unit type in BAR material costing formula.")
            return 0

    def get_quote_sheet_material_operation_total_cost(self, mom_requested_qty: int, jb_material: jb.QuoteReq,
                                                      material_master_record: jb.Material
                                                      ) -> Union[int, float, Decimal]:
        # QuoteReq attributes
        part_length = jb_material.part_length
        part_width = jb_material.part_width
        bar_end = jb_material.bar_end
        sheet_weight = jb_material.cost_unit_conv
        cost_uofm = jb_material.cost_uofm
        est_unit_cost = jb_material.est_unit_cost

        # Material master attributes
        sheet_length = material_master_record.is_length
        sheet_width = material_master_record.is_width
        last_cost = material_master_record.last_cost
        average_cost = material_master_record.average_cost
        standard_cost = material_master_record.standard_cost

        length_fit = sheet_length / (part_length + bar_end) if (part_length + bar_end) > 0 else 0
        width_fit = sheet_width / (part_width + bar_end) if (part_width + bar_end) > 0 else 0
        parts_per_sheet = round(length_fit * width_fit, 4)

        # NOTE: JB calculates this value with the make qty. We use the mom_requested_qty
        total_sheets = round(mom_requested_qty / parts_per_sheet, 4) if parts_per_sheet > 0 else 0

        # Calculate sheet cost based on units of weight (lb)
        if cost_uofm in ["lb", "Lb", "LB", "lbs", "Lbs", "LBS"]:
            # Determine the correct sheet cost to use.
            if last_cost > 0:
                sheet_cost = last_cost * sheet_weight
            elif average_cost > 0:
                sheet_cost = average_cost * sheet_weight
            elif standard_cost > 0:
                sheet_cost = standard_cost * sheet_weight
            else:
                sheet_cost = 0
                logger.info("Could not determine sheet cost. Populating 0.")
            return total_sheets * sheet_cost

        # Calculate sheet cost based on units of "per sheet" (ea)
        elif cost_uofm in ["ea", "Ea", "EA", "each", "Each", "EACH"]:
            if est_unit_cost > 0:
                return est_unit_cost * total_sheets
            elif last_cost > 0:
                return last_cost * total_sheets
            elif average_cost > 0:
                return average_cost * total_sheets
            else:
                return standard_cost * total_sheets
        else:
            logger.info("Unsupported unit type in SHEET material costing formula.")
            return 0

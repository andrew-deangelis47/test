from baseintegration.importer.import_processor import BaseImportProcessor
from epicor.quote import QuoteDetail, QuoteAssembly, QuoteMaterial
from epicor.job import JobEntry, JobAssembly, JobMaterial
from epicor.engineering_workbench import EWBRev, EWBMaterial
from epicor.importer.utils import RepeatPartUtilObject, QuoteMOMUtil, JobMOMUtil, MATERIAL_COSTING_VARS, EWBMOMUtil
from typing import List, Union
from decimal import Decimal
from baseintegration.utils.repeat_work_objects import RequiredMaterials, CostingVariable
from baseintegration.utils import safe_get, logger
from epicor.importer.epicor_client_cache import EpicorClientCache


class RequiredMaterialProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util_object: RepeatPartUtilObject, epicor_client_cache: EpicorClientCache,
                 bulk=False):
        logger.info("RequiredMaterialProcessor - Attempting to create RequiredMaterials")
        self.bulk = bulk
        if epicor_client_cache:
            self.epicor_client_cache: EpicorClientCache = epicor_client_cache
        else:
            self.epicor_client_cache: EpicorClientCache = repeat_part_util_object.epicor_client_cache

        for quote_mom_util in repeat_part_util_object.quote_mom_utils:
            quote_mom_util: QuoteMOMUtil = quote_mom_util
            quote_mom_util.mom.required_materials = self._get_quote_mom_material_operations(quote_mom_util)

        for job_mom_util in repeat_part_util_object.job_mom_utils:
            job_mom_util: JobMOMUtil = job_mom_util
            job_mom_util.mom.required_materials = self._get_job_mom_material_operations(job_mom_util)

        for ewb_mom_util in repeat_part_util_object.ewb_mom_utils:
            ewb_mom_util: EWBMOMUtil = ewb_mom_util
            ewb_mom_util.mom.required_materials = self._get_ewb_mom_material_operations(
                ewb_mom_util, repeat_part_util_object.repeat_part.part_number)

        return repeat_part_util_object

    def _get_quote_mom_material_operations(self, quote_mom_util: QuoteMOMUtil) -> List[RequiredMaterials]:
        required_materials: List[RequiredMaterials] = []
        epicor_quote_detail: QuoteDetail = quote_mom_util.epicor_quote_detail
        epicor_quote_assembly: QuoteAssembly = quote_mom_util.quote_assembly

        epicor_materials: List[QuoteMaterial] = self.get_quote_materials_from_epicor_client_cache(
            epicor_quote_detail.QuoteNum, epicor_quote_detail.QuoteLine, epicor_quote_assembly.AssemblySeq)

        for epicor_material in epicor_materials:
            if (epicor_quote_detail.QuoteNum == epicor_material.QuoteNum) and (
                epicor_quote_detail.QuoteLine == epicor_material.QuoteLine) and (
                epicor_quote_assembly.AssemblySeq == epicor_material.AssemblySeq
            ):
                required_material = RequiredMaterials(
                    name=epicor_material.PartNum,
                    notes=self._get_material_notes(epicor_material),
                    total_cost=self.get_quote_material_total_cost(quote_mom_util, epicor_material),
                    costing_variables=[],
                )
                required_material.costing_variables = self._get_costing_variables(epicor_material)
                required_materials.append(required_material)

        return required_materials

    def _get_job_mom_material_operations(self, job_mom_util: JobMOMUtil) -> List[RequiredMaterials]:
        required_materials: List[RequiredMaterials] = []
        epicor_job: JobEntry = job_mom_util.epicor_job
        epicor_job_assembly: JobAssembly = job_mom_util.job_assembly

        epicor_materials: List[JobMaterial] = self.get_job_materials_from_epicor_client_cache(
            epicor_job.JobNum, epicor_job_assembly.AssemblySeq)

        for epicor_material in epicor_materials:
            if (epicor_job.JobNum == epicor_material.JobNum) and (
                    epicor_job_assembly.AssemblySeq == epicor_material.AssemblySeq
            ):
                required_material = RequiredMaterials(
                    name=str(epicor_material.PartNum),
                    notes=self._get_material_notes(epicor_material),
                    total_cost=self.get_job_material_total_cost(epicor_material),
                    costing_variables=[]
                )
                required_material.costing_variables = self._get_costing_variables(epicor_material)
                required_materials.append(required_material)

        return required_materials

    def _get_ewb_mom_material_operations(self, ewb_mom_util: EWBMOMUtil, part_number: str) -> List[RequiredMaterials]:
        required_materials: list = []
        epicor_ewb_rev: EWBRev = ewb_mom_util.epicor_ewb_rev

        epicor_materials: List[EWBMaterial] = self.get_ewb_materials_from_epicor_client_cache(
            epicor_ewb_rev.SysRowID, part_number)

        for epicor_material in epicor_materials:
            required_material = RequiredMaterials(
                name=str(epicor_material.MtlPartNum),
                notes=self._get_material_notes(epicor_material),
                total_cost=epicor_material.EstMtlBurUnitCost,
            )
            required_material.costing_variables = self._get_costing_variables(epicor_material)
            required_materials.append(required_material)

        return required_materials

    def get_ewb_materials_from_epicor_client_cache(self, sys_row_id: str, part_number: str) -> List[EWBMaterial]:
        ewb_materials_list: List[EWBMaterial] = []
        for ewb_rev in self.epicor_client_cache.nested_ewb_rev_cache:
            if ewb_rev.SysRowID == sys_row_id:
                for ewb_material in ewb_rev.ECOMtls:
                    if ewb_material.PartNum == part_number and ewb_material.PullAsAsm is False:
                        ewb_materials_list.append(ewb_material)

        return ewb_materials_list

    def _get_material_notes(self, epicor_material: Union[QuoteMaterial, JobMaterial, EWBMaterial]) -> str:
        notes = ''
        if safe_get(epicor_material, 'Description', False):
            notes += f"Description: {epicor_material.Description}\n"
        if safe_get(epicor_material, "MfgComment", False):
            notes += f"MfgComment: {epicor_material.MfgComment}\n"
        if safe_get(epicor_material, "PurComment", False):
            notes += f"PurComment: {epicor_material.PurComment}\n"
        return notes

    def _get_costing_variables(self, epicor_material: Union[QuoteMaterial, JobMaterial, EWBMaterial]) -> List[CostingVariable]:
        costing_variables: List[CostingVariable] = []
        for variable_name, default_val in MATERIAL_COSTING_VARS.items():

            epicor_value = safe_get(epicor_material, variable_name, default_val)
            if isinstance(epicor_value, (int, float, Decimal)):
                value = float(epicor_value)
            elif isinstance(epicor_value, bool):
                value = bool(epicor_value)
            else:
                value = str(epicor_value)

            costing_var = CostingVariable(
                label=variable_name,
                value=value
            )
            costing_variables.append(costing_var)
        return costing_variables

    def get_quote_materials_from_epicor_client_cache(self, quote_num: str, quote_line: str, assembly_seq: int) -> List[QuoteMaterial]:
        quote_materials_list: List[QuoteMaterial] = []
        for quote_assembly in self.epicor_client_cache.nested_quote_assembly_cache:
            if (quote_assembly.QuoteNum == quote_num) and (quote_assembly.QuoteLine == quote_line) and (
                    quote_assembly.AssemblySeq == assembly_seq):
                quote_materials_list = quote_assembly.QuoteMtls

        return quote_materials_list

    def get_job_materials_from_epicor_client_cache(self, job_num: str, assembly_seq: int) -> List[JobMaterial]:
        job_materials_list: List[JobMaterial] = []
        for job_entry in self.epicor_client_cache.nested_job_entry_cache:
            if job_entry.JobNum == job_num:
                for job_assembly in job_entry.JobAsmbls:
                    if job_assembly.AssemblySeq == assembly_seq:
                        job_materials_list = job_assembly.JobMtls

        return job_materials_list

    def get_quote_material_total_cost(self, quote_mom_util: QuoteMOMUtil, epicor_material: QuoteMaterial):
        unit_cost = float(safe_get(epicor_material, "EstUnitCost", 0))
        qty_per = float(safe_get(epicor_material, "QtyPer", 1))
        quoted_qty = float(safe_get(quote_mom_util.epicor_quote_qty, "OurQuantity", 1))
        return unit_cost * qty_per * quoted_qty

    def get_job_material_total_cost(self, epicor_material: JobMaterial):
        unit_cost = float(safe_get(epicor_material, "EstUnitCost", 0))
        requested_qty = float(safe_get(epicor_material, "RequiredQty", 1))
        material_total_cost = unit_cost * requested_qty
        return round(material_total_cost, 3)

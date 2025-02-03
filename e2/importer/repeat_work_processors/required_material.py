from typing import List

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import safe_get, safe_get_non_null
from baseintegration.utils.repeat_work_objects import RequiredMaterials, CostingVariable
from e2.models import Estim, Materials, JobReq
from e2.importer.utils import (
    RepeatPartUtilObject,
    is_required_material_quantity,
    REQUIRED_MATERIAL_E2_MATERIAL_COSTING_VARIABLES,
    REQUIRED_MATERIAL_ESTIM_COSTING_VARIABLES, JobMOMUtil, REQUIRED_MATERIAL_JOB_REQ_COSTING_VARIABLES,
    iterate_job_requirements, iterate_template_materials
)


class RequiredMaterialProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util: RepeatPartUtilObject):
        logger.info(f"Calculating required materials on methods of manufacture for repeat work part from E2 with part number {repeat_part_util.e2_part.partno}")
        self.source_database = self._importer.source_database
        self.repeat_part_util = repeat_part_util

        for job_mom_util in repeat_part_util.job_mom_utils:
            if job_mom_util.order_detail:
                job_mom_util.method_of_manufacture.required_materials = self.get_job_mom_required_materials(job_mom_util)
            else:
                logger.info(f"Not calculating job MoM materials for part number "
                            f"{self.repeat_part_util.repeat_part.part_number} with header {job_mom_util.erp_code} "
                            f"since it is a job req")

        # we do not add materials for imported quotes

        template_required_materials: List[RequiredMaterials] = self.get_template_mom_required_materials()
        for template_mom_util in repeat_part_util.template_mom_utils:
            template_mom_util.method_of_manufacture.required_materials = template_required_materials

        return repeat_part_util

    def get_job_mom_required_materials(self, job_mom_util: JobMOMUtil) -> List[RequiredMaterials]:
        """
        - Iterates through the job requirements for the repeat part provided
        - If a subpart retrieved has a raw material product code, appends the material to a list of required materials to return
        """
        part_number = self.repeat_part_util.repeat_part.part_number

        logger.info(f"Calculating required materials for repeat work part from E2 with part number {part_number}")

        required_materials: List[RequiredMaterials] = []
        raw_material_prod_codes = self._importer.erp_config.raw_material_prod_codes

        for job_req, estim in iterate_job_requirements(self.source_database, job_mom_util):
            if job_req.prodcode in raw_material_prod_codes or is_required_material_quantity(job_req.qty2buy):
                costing_variables = [
                    *self.get_estim_costing_variables(estim),
                    *self.get_job_req_costing_variables(job_req)
                ]
                required_material = RequiredMaterials(
                    name=safe_get_non_null(job_req, "partno", "PART NUMBER"),
                    notes=self.get_required_material_notes(estim),
                    total_cost=job_req.cost,
                    costing_variables=costing_variables
                )
                required_materials.append(required_material)

        return required_materials

    def get_template_mom_required_materials(self):
        """
        - Iterates through the materials for the repeat part provided
        - If a subpart retrieved has a raw material product code, appends the material to a list of required materials to return
        """
        part_number = self.repeat_part_util.repeat_part.part_number

        logger.info(f"Calculating required materials for repeat work part from E2 with part number {part_number}")

        required_materials: List[RequiredMaterials] = []
        raw_material_prod_codes = self._importer.erp_config.raw_material_prod_codes

        for e2_material, estim in iterate_template_materials(self.source_database, part_number):
            if estim.prodcode in raw_material_prod_codes or is_required_material_quantity(e2_material.qty):
                costing_variables = [
                    *self.get_estim_costing_variables(estim),
                    *self.get_material_costing_variables(e2_material)
                ]
                required_material = RequiredMaterials(
                    name=safe_get_non_null(estim, "partno", "PART NUMBER"),
                    notes=self.get_required_material_notes(estim),
                    total_cost=e2_material.totalcost,
                    costing_variables=costing_variables
                )
                required_materials.append(required_material)

        return required_materials

    def get_required_material_notes(self, estim: Estim) -> str:
        notes = ""
        if safe_get(estim, 'descrip', False):
            notes += f"Description: {estim.descrip}\n"
        if safe_get(estim, "prodcode", False):
            notes += f"Prod Code: {estim.prodcode}\n"
        if safe_get(estim, "comments", False):
            notes += f"Comments: {estim.comments}\n"
        return notes

    def get_estim_costing_variables(self, estim: Estim):
        return [
            CostingVariable(
                label=variable_name,
                value=safe_get_non_null(estim, variable_name, default_val)
            ) for variable_name, default_val in REQUIRED_MATERIAL_ESTIM_COSTING_VARIABLES.items()
        ]

    def get_job_req_costing_variables(self, job_req: JobReq):
        return [
            CostingVariable(
                label=variable_name,
                value=safe_get_non_null(job_req, e2_field_name, default_val) if e2_field_name else default_val
            ) for variable_name, (e2_field_name, default_val) in REQUIRED_MATERIAL_JOB_REQ_COSTING_VARIABLES.items()
        ]

    def get_material_costing_variables(self, e2_material: Materials):
        return [
            CostingVariable(
                label=variable_name,
                value=safe_get_non_null(e2_material, variable_name, default_val)
            ) for variable_name, default_val in REQUIRED_MATERIAL_E2_MATERIAL_COSTING_VARIABLES.items()
        ]

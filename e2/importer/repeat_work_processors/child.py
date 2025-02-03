from typing import List

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_objects import Child
from baseintegration.utils import safe_get_non_null
from e2.importer.utils import RepeatPartUtilObject, is_required_material_quantity, JobMOMUtil, iterate_job_requirements, \
    iterate_child_order_dets, iterate_template_materials


class ChildProcessor(BaseImportProcessor):

    def _process(self, repeat_part_util: RepeatPartUtilObject, create_child_parts: bool = False) -> RepeatPartUtilObject:
        logger.info(f"Calculating children on methods of manufacture for repeat work part from E2 with part number {repeat_part_util.e2_part.partno}")
        self.source_database = self._importer.source_database
        self.repeat_part_util = repeat_part_util
        self.create_child_parts = create_child_parts
        self.raw_material_prod_codes = self._importer.erp_config.raw_material_prod_codes

        for job_mom_util in repeat_part_util.job_mom_utils:
            if job_mom_util.order_detail:
                children = [
                    *self.get_children_from_job_reqs(job_mom_util),
                    *self.get_children_from_child_order_dets(job_mom_util)
                ]
                job_mom_util.method_of_manufacture.children = children
            else:
                logger.info(f"Not calculating job MoM children for part number "
                            f"{self.repeat_part_util.repeat_part.part_number} with header {job_mom_util.erp_code} "
                            f"since it is a job req")

        # we do not add children for imported quotes

        template_children = self.get_template_children()
        for template_mom_util in repeat_part_util.template_mom_utils:
            template_mom_util.method_of_manufacture.children = template_children

        return repeat_part_util

    def get_children_from_job_reqs(self, job_mom_util: JobMOMUtil) -> List[Child]:
        """
        - Iterates through the job requirements for the repeat part provided
        - If a subpart retrieved does not have a raw material product code, appends the material to a list of children to return
        """
        logger.info(f"Calculating job children from job reqs of part number {self.repeat_part_util.repeat_part.part_number} with header {job_mom_util.erp_code}")

        children: List[Child] = []

        for job_req, estim in iterate_job_requirements(self.source_database, job_mom_util):
            if job_req.prodcode not in self.raw_material_prod_codes and not is_required_material_quantity(job_req.qty2buy):
                self.process_child_repeat_part(estim.partno)
                child = Child(
                    part_number=estim.partno,
                    revision=safe_get_non_null(estim, "revision", ""),
                    qty_per_parent=(job_req.qty2buy or 1) / (job_mom_util.order_detail.qty_ordered or 1)
                )
                children.append(child)

        return children

    def get_children_from_child_order_dets(self, job_mom_util: JobMOMUtil) -> List[Child]:
        """
        - Iterates through the child order dets for the repeat part provided
        - If a subpart retrieved does not have a raw material product code, appends the material to a list of children to return
        """
        logger.info(f"Calculating job children from child order dets of part number {self.repeat_part_util.repeat_part.part_number} with header {job_mom_util.erp_code}")

        children: List[Child] = []

        for child_order_det, estim in iterate_child_order_dets(self.source_database, job_mom_util):
            self.process_child_repeat_part(estim.partno)
            child = Child(
                part_number=estim.partno,
                revision=safe_get_non_null(estim, "revision", ""),
                qty_per_parent=(child_order_det.qty_ordered or 1) / (job_mom_util.order_detail.qty_ordered or 1)
            )
            children.append(child)

        return children

    def get_template_children(self):
        """
        - Iterates through the materials for the repeat part provided
        - If a subpart retrieved does not have a raw material product code, appends the material to a list of children to return
        """
        part_number = self.repeat_part_util.repeat_part.part_number
        logger.info(f"Calculating template children of part number {self.repeat_part_util.repeat_part.part_number}")

        children: List[Child] = []

        for e2_material, estim in iterate_template_materials(self.source_database, part_number):
            if estim.prodcode not in self.raw_material_prod_codes and not is_required_material_quantity(e2_material.qty):
                self.process_child_repeat_part(estim.partno)
                child = Child(
                    part_number=estim.partno,
                    revision=safe_get_non_null(estim, "revision", ""),
                    qty_per_parent=e2_material.qty or 1
                )
                children.append(child)

        return children

    def process_child_repeat_part(self, child_part_number: str):
        if self.create_child_parts and child_part_number:
            logger.info(f"Creating child parts for part number {child_part_number} with parent {self.repeat_part_util.e2_part.partno}")
            self._importer._process_repeat_part(child_part_number, create_child_parts=True)

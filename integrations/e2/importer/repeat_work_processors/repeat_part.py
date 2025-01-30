import datetime
from typing import List

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_objects import Part as RepeatPart
from e2.models import Estim, Materials
from e2.importer.utils import RepeatPartUtilObject, is_required_material_quantity


class RepeatPartImportProcessor(BaseImportProcessor):

    def _process(self, repeat_part_number: str) -> RepeatPartUtilObject:
        logger.info(f"Processing repeat work part from E2 with part number {repeat_part_number}")
        self.source_database = self._importer.source_database

        e2_part_list: List[Estim] = Estim.objects.using(self.source_database).filter(partno=repeat_part_number)
        if not e2_part_list:
            logger.info(f"Repeat work import failed - unable to find part with part number {repeat_part_number} in E2")
            return None

        e2_part: Estim = e2_part_list[0]
        e2_part_revision: str = e2_part.revision if e2_part.revision else ""

        repeat_part = RepeatPart(
            part_number=repeat_part_number,
            revision=e2_part_revision,
            erp_name="e2",
            is_root=self.is_root(e2_part),
            import_date=int(datetime.datetime.now().timestamp()),
            headers=[],
            type=self.get_part_type(e2_part),
            size_x=0.0,
            size_y=0.0,
            size_z=0.0,
            area=0.0,
            thickness=0.0,
            filename=e2_part.drawingfilename
        )

        repeat_part_util = RepeatPartUtilObject(repeat_part, e2_part)
        logger.info(f"Created repeat part object for E2 part number {repeat_part_number}")
        return repeat_part_util

    def is_root(self, e2_part: Estim) -> bool:
        root_instances_query_set = Materials.objects.using(self.source_database).filter(partno=e2_part.partno)
        return len(root_instances_query_set) > 0

    def get_part_type(self, e2_part: Estim) -> str:
        parent_parts_query_set = Materials.objects.using(self.source_database).filter(subpartno=e2_part.partno)
        purchased_nums: List[int] = parent_parts_query_set.values_list('purchased', flat=True)
        if 1 in purchased_nums:
            return "purchased"

        # determine if the part has child components
        raw_material_prod_codes = self._importer.erp_config.raw_material_prod_codes
        child_parts_query_set = Materials.objects.using(self.source_database).filter(partno=e2_part.partno)
        child_part_list = []
        for child_part in child_parts_query_set:
            child_part: Materials
            if not is_required_material_quantity(child_part.qty or 0):
                child_part_list.append(child_part.subpartno)
        child_estims = Estim.objects.using(self.source_database)\
            .filter(partno__in=child_part_list)\
            .exclude(prodcode__in=raw_material_prod_codes)

        if child_estims.count() > 0:
            return "assembled"
        else:
            return "manufactured"

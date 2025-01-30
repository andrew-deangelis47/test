from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.repeat_work_objects import Part
from baseintegration.datamigration import logger
from inforsyteline.importer.configuration import RepeatPartImportConfig
from inforsyteline.importer.repeat_work_utils import get_product_code
from inforsyteline.models import ItemMst, JobMst


class RepeatPartProcessor(BaseImportProcessor):
    def _process(self, repeat_part_id) -> Part:
        logger.info(f"Creating repeat part from Inforsyteline item ID: {repeat_part_id}")
        self.source_database = self._importer.source_database
        size_x = 0
        size_y = 0
        thickness = 0
        area = 0
        revision = ""
        record = self.get_record(repeat_part_id)
        if not record:
            raise Exception(f"Part with ID {repeat_part_id} not found in Infor Syteline")
        if isinstance(record, ItemMst):
            item: ItemMst = record
            size_x = item.pp_width_linear_dimension
            size_y = item.pp_length_linear_dimension
            thickness = item.pp_height_linear_dimension
            area = item.pp_area
            revision = item.revision
        return Part(
            part_number=repeat_part_id,
            revision=revision,
            type=self.get_part_type(record),
            erp_name="inforsyteline",
            is_root=self.is_root(repeat_part_id),
            size_x=size_x,
            size_y=size_y,
            thickness=thickness,
            area=area
        )

    def get_record(self, repeat_part_id):
        item: ItemMst = ItemMst.objects.using(self.source_database).filter(item=repeat_part_id).first()
        if item:
            return item
        job: JobMst = JobMst.objects.using(self.source_database).filter(item=repeat_part_id)
        if job:
            return job

    def get_part_type(self, item: ItemMst) -> str:
        if isinstance(item, ItemMst):
            config: RepeatPartImportConfig = self._importer.erp_config
            if get_product_code(item, self.source_database) in config.purchased_component_product_codes:
                return "purchased"
        return "manufactured"  # this may be updated in the method of manufacture processor

    def is_root(self, repeat_part_id) -> bool:
        is_root_job = JobMst.objects.using(self.source_database).filter(item=repeat_part_id, ref_job=None).exists()
        return is_root_job

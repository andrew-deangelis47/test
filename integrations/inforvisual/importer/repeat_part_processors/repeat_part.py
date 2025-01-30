from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from inforvisual.importer.repeat_part_processors.repeat_work_utils import PartData
from inforvisual.models import (
    Part as InforVisualPart,
)
from baseintegration.utils.repeat_work_objects import Part
import datetime


class RepeatPartImportProcessor(BaseImportProcessor):
    def _process(self, repeat_part_number: str, headers: list, part_data: PartData) -> dict:
        logger.info(f"Creating repeat part from item ID: {repeat_part_number}")
        self.source_database = self._importer.source_database
        part: InforVisualPart = InforVisualPart.objects.using(self.source_database)\
            .filter(id=repeat_part_number).first()
        if part:
            revision = part.revision_id
            part_type = "purchased" if part.purchased == "Y" else part_data.part_type
        else:
            revision = ""
            part_type = part_data.part_type
        repeat_part = Part(
            part_number=repeat_part_number,
            revision=revision,
            erp_name="inforvisual",
            is_root=part_data.is_root,
            import_date=int(datetime.datetime.now().timestamp()),
            headers=headers,
            type=part_type,
            size_x=0.0,
            size_y=0.0,
            size_z=0.0,
            area=0.0,
            thickness=0.0,
            filename=repeat_part_number,
        ).to_json()
        return repeat_part

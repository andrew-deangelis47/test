from typing import Union

from baseintegration.utils.repeat_work_objects import Part
from baseintegration.datamigration import logger
from m2m.importer.processors.base import BaseM2MImportProcessor
from m2m.models import Inmastx, InmastExt, Qtitem, Jomast, Jodbom, Qtdbom, Inbomm
from m2m.utils.repeat_work_utils import PartData


class RepeatPartProcessor(BaseM2MImportProcessor):
    def _process(self, repeat_part_id) -> (Part, PartData):
        self.source_database = self._importer.source_database
        part_data = self.get_part_data(repeat_part_id)

        logger.info(f"Creating repeat part from M2M item ID: {part_data.id()}")
        size_x = 0
        size_y = 0
        thickness = 0
        if type(part_data.entry) is Inmastx:
            item_extension: InmastExt = InmastExt.objects.using(self.source_database)\
                .filter(fkey_id=part_data.entry.identity_column).first()
            if item_extension:
                size_x = self.generate_normalized_value(item_extension.dimlength) or 0
                size_y = self.generate_normalized_value(item_extension.dimwidth) or 0
                thickness = self.generate_normalized_value(item_extension.mtlthickness) or 0

        repeat_part = Part(
            part_number=self.generate_normalized_value(part_data.part_number),
            revision=self.generate_normalized_value(part_data.revision),
            type=self.get_part_type(part_data),
            erp_name="m2m",
            is_root=self.is_root(part_data),
            size_x=size_x,
            size_y=size_y,
            thickness=thickness,
            area=0
        )

        return repeat_part, part_data

    def get_part_type(self, part_data: PartData) -> str:
        return "manufactured"  # this is potentially changed later, in the method of manufacture processor

    def get_part_data(self, repeat_part_id: Union[str, tuple[str, str]]) -> PartData:
        if isinstance(repeat_part_id, tuple):
            part_number, revision = repeat_part_id
        else:
            part_number = repeat_part_id
            revision = None

        # check for matching item master entries
        if revision is None:
            item: Inmastx = Inmastx.objects.using(self.source_database).filter(fpartno=part_number).first()
        else:
            item: Inmastx = Inmastx.objects.using(self.source_database).filter(
                fpartno=part_number, frev=revision).first()
        if item:
            return PartData(entry=item, part_number=item.fpartno, revision=item.frev)

        # check for matching quote item entries
        if revision is None:
            quote_item: Qtitem = Qtitem.objects.using(self.source_database).filter(fpartno=part_number).first()
        else:
            quote_item: Qtitem = Qtitem.objects.using(self.source_database).filter(
                fpartno=part_number, fpartrev=revision).first()
        if quote_item:
            return PartData(entry=quote_item, part_number=quote_item.fpartno, revision=quote_item.fpartrev)

        # check for matching job entries
        if revision is None:
            job_item: Jomast = Jomast.objects.using(self.source_database).filter(fpartno=part_number).first()
        else:
            job_item: Jomast = Jomast.objects.using(self.source_database).filter(
                fpartno=part_number, fpartrev=revision).first()
        if job_item:
            return PartData(entry=job_item, part_number=job_item.fpartno, revision=job_item.fpartrev)

        # check for matching quote bom line entries
        if revision is None:
            quote_bom: Qtdbom = Qtdbom.objects.using(self.source_database).filter(fbompart=part_number).first()
        else:
            quote_bom: Qtdbom = Qtdbom.objects.using(self.source_database).filter(
                fbompart=part_number, fbomrev=revision).first()
        if quote_bom:
            return PartData(entry=quote_bom, part_number=quote_bom.fbompart, revision=quote_bom.fbomrev)

        # check for matching job bom line entries
        if revision is None:
            job_bom: Jodbom = Jodbom.objects.using(self.source_database).filter(fbompart=part_number).first()
        else:
            job_bom: Jodbom = Jodbom.objects.using(self.source_database)\
                .filter(fbompart=part_number, fbomrev=revision).first()
        if job_bom:
            return PartData(entry=job_bom, part_number=job_bom.fbompart, revision=job_bom.fbomrev)

        if revision is None:
            raise Exception(f"Could not find part {part_number} in M2M")
        else:
            raise Exception(f"Could not find part {part_number} with revision {revision} in M2M")

    def is_root(self, part_data: PartData) -> bool:
        # check if it is a root standard BOM
        standard_boms = Inbomm.objects.using(self.source_database)\
            .filter(fpartno=part_data.part_number, fcpartrev=part_data.revision)
        if standard_boms.exists():
            return True

        # check if it is a root quote item
        quote_items = Qtitem.objects.using(self.source_database).filter(
            fpartno=part_data.part_number, fpartrev=part_data.revision)
        if quote_items.exists():
            return True

        # check if it is a root job
        jobs = Jomast.objects.using(self.source_database).filter(
            fpartno=part_data.part_number, fpartrev=part_data.revision, fsub_from='')
        if jobs.exists():
            return True

        return False

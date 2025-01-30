from .base_extractor import BaseExtractor
from sage.models.sage_models.work_center import WorkCenter, WorkCenterExtraInfo, WorkCenterFullEntity


class WorkCenterExtractor(BaseExtractor):
    primary_table_key = 'E'

    def get_work_centers(self, i_file: str):
        raw_full_work_centers = self.extract_full_entities(i_file)
        full_work_center_objects = []

        for raw_full_work_center in raw_full_work_centers:
            work_center = self.extract_entities(raw_full_work_center, 'E', WorkCenter)[0]
            extra_info = self.extract_entities(raw_full_work_center, 'T', WorkCenterExtraInfo)[0]

            full_work_center_objects.append(
                WorkCenterFullEntity(work_center=work_center, extra_info=extra_info)
            )

        return full_work_center_objects

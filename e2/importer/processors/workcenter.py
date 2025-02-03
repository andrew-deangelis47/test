from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
from e2.models import Workcntr
from baseintegration.utils.custom_table import ImportCustomTable
from e2.utils import get_version_number


class WorkCenterBulkImportProcessor(BaseImportProcessor):

    def _process(self, wc_ids: List[str]) -> bool:  # noqa: C901
        work_centers: List[dict] = []
        for wc_id in wc_ids:
            base_dict = self._importer.header_dict.copy()
            wc_mst_row = Workcntr.objects.filter(workcntr=wc_id).first()
            if not wc_mst_row:
                logger.info(f"Was not able to import {wc_mst_row} as it could not be found in the wc table, skipping")
                continue
            dict_to_upload = self.get_wc(wc_mst_row, base_dict)
            if dict_to_upload:
                headers = ImportCustomTable.assemble_custom_headers(dict_to_upload)
                new_record = ImportCustomTable.generate_custom_header_nr(dict_to_upload, headers)
                work_centers.append(new_record)
        result: dict = ImportCustomTable.upload_records(
            identifier=f'E2-work-center-bulk-upload-count-{len(work_centers)}',
            table_name=self._importer.table_name,
            records=work_centers)
        return len(result["failures"]) == 0

    def get_wc(self, wc_mst_row: Workcntr, base_dict: dict):  # noqa: C901
        base_dict["WorkCntr"] = wc_mst_row.workcntr
        base_dict["ShortName"] = wc_mst_row.shortname
        base_dict["Descrip"] = wc_mst_row.descrip
        base_dict["BurdenRate"] = wc_mst_row.burdenrate
        base_dict["LaborRate"] = wc_mst_row.laborrate
        base_dict["Cycle1"] = wc_mst_row.cycle1
        base_dict["Setup1"] = wc_mst_row.setup1
        if get_version_number() == "default":
            base_dict["LastModDate"] = wc_mst_row.lastmoddate if wc_mst_row.lastmoddate is not None else ""
        return base_dict


class WorkCenterImportProcessor(WorkCenterBulkImportProcessor):
    def _process(self, wc_id: str) -> bool:
        return super()._process([wc_id])


class WorkCenterBulkPlaceholder:
    pass

from baseintegration.importer.import_processor import BaseImportProcessor
from jobboss.models import WorkCenter
from baseintegration.utils.custom_table import ImportCustomTable
from paperless.client import PaperlessClient
from baseintegration.utils import custom_table_patch


class WorkCenterImportProcessor(BaseImportProcessor):

    def _process(self, wc_id: str):  # noqa: C901
        base_dict = self._importer.header_dict.copy()
        wc_mst_row = WorkCenter.objects.filter(work_center=wc_id).first()
        if not wc_mst_row:
            raise Exception(f"Was not able to import {wc_mst_row} as it could not be found in the wc table")
        dict_to_upload = self.get_wc(wc_mst_row, base_dict)
        if dict_to_upload:
            headers = ImportCustomTable.assemble_custom_headers(dict_to_upload)
            new_record = ImportCustomTable.generate_custom_header_nr(dict_to_upload, headers)
            data = dict(row_data=new_record)
            client = PaperlessClient.get_instance()
            url = f"suppliers/public/custom_tables/{self._importer.table_name}/row"
            custom_table_patch(client=client, data=data, url=url, identifier=wc_id)

    def get_wc(self, wc_mst_row: WorkCenter, base_dict: dict):  # noqa: C901
        base_dict["work_center"] = wc_mst_row.work_center
        base_dict["type"] = wc_mst_row.type
        base_dict["setup_labor_rate"] = wc_mst_row.setup_labor_rate
        base_dict["run_labor_rate"] = wc_mst_row.run_labor_rate
        base_dict["labor_burden"] = wc_mst_row.labor_burden
        base_dict["machine_burden"] = wc_mst_row.machine_burden
        base_dict["ga_burden"] = wc_mst_row.ga_burden
        return base_dict

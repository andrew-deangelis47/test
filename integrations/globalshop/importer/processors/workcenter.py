from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import custom_table_patch
from baseintegration.utils.custom_table import ImportCustomTable
from paperless.client import PaperlessClient

from baseintegration.utils.data import safe_trim
from globalshop.workcenter import WorkCenter, WorkCenterRecord


class WorkCenterImportProcessor(BaseImportProcessor):

    def _process(self, wc_id: str):
        logger.info("Calling workcenter process method")
        wc_dict = self.get_wc(wc_id, self._importer.header_dict.copy())
        if wc_dict:
            logger.info(wc_dict)
            headers = ImportCustomTable.assemble_custom_headers(wc_dict)
            new_record = ImportCustomTable.generate_custom_header_nr(wc_dict, headers)
            data = dict(row_data=new_record)
            client = PaperlessClient.get_instance()
            url = "suppliers/public/custom_tables/gss_workcenters/row"
            custom_table_patch(client=client, data=data, url=url, identifier=wc_id)

    def get_wc(self, wc_id: str, base_dict: dict) -> dict:
        wc: WorkCenterRecord = WorkCenter.get(workcenter_id=wc_id)
        logger.info(f"WorkCenter is : {wc}")

        base_dict["workcenter"] = safe_trim(wc.workcenter) if wc.workcenter is not None else ''
        base_dict["wc_dept"] = wc.wc_dept if wc.wc_dept is not None else ''
        base_dict["standard_bill"] = wc.standard_bill if wc.standard_bill is not None else ''
        base_dict["standard_cost"] = wc.standard_cost if wc.standard_cost is not None else ''
        base_dict["standard_overhead"] = wc.standard_overhead if wc.standard_overhead is not None else ''
        base_dict["fixed_ovhd"] = wc.fixed_ovhd if wc.fixed_ovhd is not None else ''
        base_dict["wc_name"] = wc.wc_name if wc.wc_name is not None else ''
        base_dict["workgroup"] = wc.workgroup if wc.workgroup is not None else ''
        base_dict["workgroup_descr"] = wc.workgroup_descr if wc.workgroup_descr is not None else ''
        base_dict["prototype_wc"] = wc.prototype_wc if wc.prototype_wc is not None else ''
        return base_dict

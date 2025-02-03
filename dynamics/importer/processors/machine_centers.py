from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.exporter.order_exporter import logger
from baseintegration.utils.custom_table import ImportCustomTable

from dynamics.exceptions import DynamicsNotFoundException
from dynamics.importer.utils import DynamicsToPaperlessTranslator
from dynamics.objects.item import MachineCenter


class DynamicsMachineCenterBulkImportProcessor(BaseImportProcessor):

    def _process(self, machine_center_nos: List[str]) -> bool:
        machine_centers: List[dict] = []
        for machine_center_no in machine_center_nos:
            machine_center: MachineCenter
            try:
                machine_center = MachineCenter.get_first({
                    'No': machine_center_no
                })
            except DynamicsNotFoundException:
                logger.info(f"Machine center '{machine_center_no}' not found in Dynamics, skipping")
                continue
            machine_center_dict = self._importer.header_dict
            DynamicsToPaperlessTranslator.update_machine_center(machine_center_dict, machine_center)
            headers = ImportCustomTable.assemble_custom_headers(machine_center_dict)
            new_record = ImportCustomTable.generate_custom_header_nr(machine_center_dict, headers)
            machine_centers.append(new_record)
        result: dict = ImportCustomTable.upload_records(
            identifier=f'dynamics-machine-center-bulk-upload-count-{len(machine_centers)}',
            table_name=self._importer.table_name,
            records=machine_centers)
        return len(result["failures"]) == 0


class DynamicsMachineCenterImportProcessor(DynamicsMachineCenterBulkImportProcessor):
    def _process(self, machine_center_no: str) -> bool:
        return super()._process([machine_center_no])


class MachineCenterBulkPlaceholder:
    pass

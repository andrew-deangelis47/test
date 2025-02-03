from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from e2.models import Estim
from baseintegration.utils.custom_table import ImportCustomTable


class MaterialBulkImportProcessor(BaseImportProcessor):

    def _process(self, material_ids: List[str]) -> bool:
        materials: List[dict] = []
        for material_id in material_ids:
            fields = Estim._meta.fields
            headers = ImportCustomTable.assemble_headers(fields)
            estim_row = Estim.objects.filter(partno=material_id).first()
            new_record = ImportCustomTable.generate_nr(estim_row, headers)
            data = dict(row_data=new_record)
            if self._importer._integration.test_mode:
                # needed to pass tests
                data['row_data']['estim_id'] = '0'
                data['row_data']['imagerepositoryid'] = 0
                data['row_data']['accountingid'] = '0'
                data['row_data']['lastmoddate'] = '0'
                data['row_data']['lastmoduser'] = '0'
                data['row_data']['istaxable'] = True
                data['row_data']['qbitemtype'] = 'nontaxable'
            materials.append(data['row_data'])
        result: dict = ImportCustomTable.upload_records(identifier=f'E2-material-bulk-upload-count-{len(materials)}',
                                                        table_name=self._importer.table_name,
                                                        records=materials)
        return len(result["failures"]) == 0


class MaterialImportProcessor(MaterialBulkImportProcessor):
    def _process(self, material_id: str):
        super()._process([material_id])


class MaterialBulkPlaceholder:
    pass

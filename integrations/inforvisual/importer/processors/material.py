from typing import List

from decimal import Decimal

from baseintegration.importer.import_processor import BaseImportProcessor
from inforvisual import models
from inforvisual.models import Part
from baseintegration.utils.custom_table import ImportCustomTable
from baseintegration.utils import safe_get
from baseintegration.datamigration import logger


class MaterialBulkImportProcessor(BaseImportProcessor):

    def _process(self, material_ids: List[str]) -> bool:  # noqa: C901
        materials: List[dict] = []
        for material_id in material_ids:
            base_dict = self._importer.header_dict.copy()
            item_mst_row = Part.objects.filter(id=material_id).first()
            if not item_mst_row:
                logger.info(f"Was not able to import {material_id} as it could not be found in the item table")
                continue
            dict_to_upload = self.get_raw_material(item_mst_row, base_dict)
            if dict_to_upload:
                headers = ImportCustomTable.assemble_custom_headers(dict_to_upload)
                new_record = ImportCustomTable.generate_custom_header_nr(dict_to_upload, headers)
                materials.append(new_record)

        result: dict = ImportCustomTable.upload_records(
            identifier=f'Inforvisual-material-bulk-upload-count-{len(materials)}',
            table_name=self._importer.table_name,
            records=materials)
        return len(result["failures"]) == 0

    def get_raw_material(self, item_mst_row: Part, base_dict: dict):  # noqa: C901
        """
        The imported columns are determined dynamically from the config.
        """
        table_name_to_instance = self.get_table_names_to_instances(part=item_mst_row)

        for column_data in self._importer.erp_config.imported_columns:
            column_name = column_data['column_name']
            source_table_name = column_data.get('source_table', 'Part')
            source_model_instance = table_name_to_instance[source_table_name]
            source_column = column_data.get('source_column', column_name)
            value = safe_get(source_model_instance, source_column)
            if isinstance(value, Decimal):
                value = float(value)
            base_dict[column_name] = value

        return base_dict

    def get_table_names_to_instances(self, part: Part):
        """
        Returns a dictionary that maps Infor table name to the relevant model instance.
        Only includes tables referenced in the customer's config.
        """
        table_name_to_instance = {
            'Part': part
        }
        used_tables = [column_data.get('source_table', 'Part')
                       for column_data in self._importer.erp_config.imported_columns]
        for table_name in used_tables:
            if table_name not in table_name_to_instance:
                # assume table has a "part" foreign key that ties it to the Part table
                model = safe_get(models, table_name)
                instance = model.objects.filter(part_id=part.id).first()
                if not instance:
                    raise Exception(f"{table_name} not found for {part.id}. Moving on")
                table_name_to_instance[table_name] = instance

        return table_name_to_instance


class MaterialImportProcessor(MaterialBulkImportProcessor):
    def _process(self, material_id: str) -> bool:
        super()._process([material_id])


class MaterialBulkPlaceholder:
    pass

from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.exporter.order_exporter import logger
from baseintegration.utils.custom_table import ImportCustomTable

from dynamics.exceptions import DynamicsNotFoundException
from dynamics.importer.utils import DynamicsToPaperlessTranslator
from dynamics.objects.item import Material, CoatingItem


class DynamicsBulkMaterialImportProcessor(BaseImportProcessor):

    def _process(self, material_ids: List[str]) -> bool:
        materials: List[dict] = []
        coating_items: List[dict] = []
        for material_id in material_ids:
            material_dict: dict
            pp_table_name: str
            try:
                material = Material.get_first({
                    'No': material_id
                })
                pp_table_name = self._importer.materials_table_name
                material_dict = self._importer.header_dict[pp_table_name]
                DynamicsToPaperlessTranslator.update_material(material_dict, material)
            except DynamicsNotFoundException:
                try:
                    material = CoatingItem.get_first({
                        'No': material_id
                    })
                    pp_table_name = self._importer.coating_items_table_name
                    material_dict = self._importer.header_dict[pp_table_name]
                    DynamicsToPaperlessTranslator.update_coating_item(material_dict, material)
                except DynamicsNotFoundException:
                    logger.info(f"Material '{material_id}' not found in Dynamics, skipping")
                    continue

            headers = ImportCustomTable.assemble_custom_headers(material_dict)
            new_record = ImportCustomTable.generate_custom_header_nr(material_dict, headers)
            if pp_table_name == self._importer.coating_items_table_name:
                coating_items.append(new_record)
            else:
                materials.append(new_record)

        material_result: dict = ImportCustomTable.upload_records(
            identifier=f'dynamics-material-bulk-upload-count-{len(materials)}',
            table_name=self._importer.materials_table_name,
            records=materials)
        coating_item_result: dict = ImportCustomTable.upload_records(
            identifier=f'dynamics-coating-item-bulk-upload-count-{len(coating_items)}',
            table_name=self._importer.coating_items_table_name,
            records=coating_items)
        failures = material_result["failures"] + coating_item_result["failures"]
        return len(failures) == 0


class DynamicsMaterialImportProcessor(DynamicsBulkMaterialImportProcessor):
    def _process(self, material_id: str) -> bool:
        return super()._process([material_id])


class DynamicsMaterialBulkPlaceholder:
    pass

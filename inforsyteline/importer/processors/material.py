from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from inforsyteline.models import ItemMst
from baseintegration.utils.custom_table import ImportCustomTable
from baseintegration.datamigration import logger
from inforsyteline.importer.repeat_work_utils import get_product_code


class MaterialBulkImportProcessor(BaseImportProcessor):

    def _process(self, material_ids: List[str]) -> bool:  # noqa: C901
        materials: List[dict] = []
        for material_id in material_ids:
            base_dict = self._importer.header_dict.copy()
            item_mst_row = ItemMst.objects.filter(item=material_id).first()
            if not item_mst_row:
                logger.info(f"Was not able to import {material_id} as it could not be found in the item table. Skipping")
                continue
            dict_to_upload = self.get_raw_material(item_mst_row, base_dict)
            if dict_to_upload:
                headers = ImportCustomTable.assemble_custom_headers(dict_to_upload)
                new_record = ImportCustomTable.generate_custom_header_nr(dict_to_upload, headers)
                materials.append(new_record)
        result: dict = ImportCustomTable.upload_records(
            identifier=f'Inforsyteline-material-bulk-upload-count-{len(materials)}',
            table_name=self._importer.table_name,
            records=materials)
        return len(result["failures"]) == 0

    def get_raw_material(self, item_mst_row: ItemMst, base_dict: dict):  # noqa: C901
        base_dict["Item"] = item_mst_row.item
        base_dict["Description"] = item_mst_row.description
        base_dict["ecn"] = str(item_mst_row.track_ecn)
        base_dict["buyer"] = item_mst_row.buyer
        base_dict["stocked"] = item_mst_row.stocked
        base_dict["u_m"] = item_mst_row.u_m
        base_dict["type"] = item_mst_row.matl_type
        base_dict["product_code"] = get_product_code(item_mst_row)
        base_dict["abc_code"] = item_mst_row.abc_code
        base_dict["cost_type"] = item_mst_row.cost_type
        base_dict["cost_method"] = item_mst_row.cost_method
        base_dict["unit_cost"] = float(item_mst_row.unit_cost)
        base_dict["current_unit_cost"] = float(item_mst_row.cur_u_cost)
        base_dict["lot_size"] = int(item_mst_row.lot_size)
        base_dict["unit_weight"] = float(item_mst_row.unit_weight)
        base_dict["weight_units"] = item_mst_row.weight_units
        return base_dict


class MaterialImportProcessor(MaterialBulkImportProcessor):

    def _process(self, material_id: str) -> bool:
        super()._process([material_id])


class MaterialBulkPlaceholder:
    pass

from typing import List

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
import jobboss.models as jb
from baseintegration.utils.custom_table import ImportCustomTable
from baseintegration.utils import safe_get


class MaterialBulkImportProcessor(BaseImportProcessor):

    def _process(self, material_ids: List[str]) -> bool:
        logger.info("Calling process method")
        materials: List[dict] = []
        for material_id in material_ids:
            material_dict = self.get_raw_material(material_id, self._importer.header_dict)
            if material_dict:
                headers = ImportCustomTable.assemble_custom_headers(material_dict)
                new_record = ImportCustomTable.generate_custom_header_nr(material_dict, headers)
                materials.append(new_record)
        result: dict = ImportCustomTable.upload_records(
            identifier=f'Jobboss-material-bulk-upload-count-{len(materials)}',
            table_name='jobboss_materials',
            records=materials)
        return len(result["failures"]) == 0

    @staticmethod
    def get_material_types_to_process():
        return ['R']

    def get_raw_material(self, material_id: str, header_dict):
        mat: jb.Material = jb.Material.objects.no_truncate_filter(material=material_id, status="Active").last()
        logger.info(f"Material is : {mat}")
        if mat is None:
            logger.info(f"Material id '{material_id}' is 'INACTIVE'")
            return None
        elif mat.type not in self.get_material_types_to_process():
            logger.info(f"Material id '{material_id}' is type '{mat.type}' - SKIPPING")
            return
        else:
            row = {
                'jb_material_id': mat.material,
                'mat_shape': mat.shape_id,
                'class': mat.class_field,
                'mat_type': mat.type,
                'mat_desc': self.get_full_material_description(mat),
                'last_updated': mat.last_updated,
                'pick_buy_indicator': mat.pick_buy_indicator,
                'rev': mat.rev
            }
            stock_item, stock_item_attributes = self.get_stock_item_attributes(mat)
            cost_attributes = self.get_cost_attributes(mat)
            mat_dimensions = self.get_material_dimensions(mat)
            shape_attributes = self.get_shape_attributes(mat)
            vendor_attributes = self.get_vendor_attributes(mat)
            dimension_attributes = self.get_stock_item_dimensions(stock_item)
            row.update(cost_attributes)
            row.update(mat_dimensions)
            row.update(stock_item_attributes)
            row.update(shape_attributes)
            row.update(vendor_attributes)
            row.update(dimension_attributes)
            for key, value in row.items():
                if key in header_dict:
                    header_dict[key] = value
            return header_dict

    @staticmethod
    def get_cost_attributes(jb_material):
        attributes = {
            'standard_cost': jb_material.standard_cost if jb_material.standard_cost is not None else 0,
            'avg_cost': jb_material.average_cost if jb_material.average_cost is not None else 0,
            'last_cost': jb_material.last_cost if jb_material.last_cost is not None else 0,
            'cost_uofm': jb_material.cost_uofm if jb_material.cost_uofm is not None else 0,
        }
        return attributes

    @staticmethod
    def get_material_dimensions(jb_material):
        attributes = {
            'IS_length': jb_material.is_length if jb_material.is_length is not None else 0,
            'IS_width': jb_material.is_width if jb_material.is_width is not None else 0,
            'IS_thickness': jb_material.is_thickness if jb_material.is_thickness is not None else 0,
        }
        return attributes

    @staticmethod
    def get_stock_item_attributes(jb_material):
        attributes = {
            'stocked_uofm': "N/A",
            'alloy': "N/A",
            'density': 0
        }
        stock_item = jb.StockItem.objects.filter(stock_item=jb_material.stock_item).first()
        raw_stock_weight = jb.RawStockWeight.objects.filter(
            class_field=jb_material.class_field
        ).order_by('-last_updated').first()
        if stock_item is not None:
            attributes = {
                'stocked_uofm': stock_item.stocked_uofm if not None else 'N/A',
                'alloy': stock_item.alloy if not None else 'N/A',
            }
        if raw_stock_weight is not None:
            attributes["density"] = raw_stock_weight.lbs_per_cu_in if not None else 0
        return stock_item, attributes

    @staticmethod
    def get_shape_attributes(jb_material):
        attributes = {
            "shape": "N/A"
        }
        shape_obj = safe_get(jb_material, 'shape')
        if shape_obj:
            attributes = {
                'shape': str(shape_obj.shape)
            }
        return attributes

    @staticmethod
    def get_vendor_attributes(jb_material):
        attributes = {
            "primary_vendor": "N/A"
        }
        vendor_obj = jb_material.primary_vendor
        if vendor_obj:
            attributes = {
                'primary_vendor': vendor_obj.vendor if not None else 'N/A'
            }
        return attributes

    @staticmethod
    def get_full_material_description(jb_material):
        notes = ""
        if jb_material.description and jb_material.ext_description:
            notes = jb_material.description + " " + jb_material.ext_description
        elif jb_material.description:
            notes = jb_material.description
        elif jb_material.ext_description:
            notes = jb_material.ext_description
        return notes

    @staticmethod
    def get_stock_item_dimensions(stock_item):
        dims = {
            'dimension1_name': "None",
            'dimension1': 0,
            'dimension2_name': "None",
            'dimension2': 0,
            'dimension3_name': "None",
            'dimension3': 0,
        }
        if stock_item is not None:
            shape_dimensions = jb.ShapeDimension.objects.filter(shape=stock_item.shape)
            for dimension in shape_dimensions:
                if dimension.db_field_name == "Dimension_1":
                    dims["dimension1_name"] = dimension.dimension if not None else 'None'
                    dims["dimension1"] = stock_item.dimension_1 if not None else 0
                elif dimension.db_field_name == "Dimension_2":
                    dims["dimension2_name"] = dimension.dimension if not None else 'None'
                    dims["dimension2"] = stock_item.dimension_2 if not None else 0
                elif dimension.db_field_name == "Dimension_3":
                    dims["dimension3_name"] = dimension.dimension if not None else 'None'
                    dims["dimension3"] = stock_item.dimension_3 if not None else 0
        return dims


class MaterialImportProcessor(MaterialBulkImportProcessor):
    def _process(self, material_id: str) -> bool:
        return super()._process([material_id])


class MaterialBulkPlaceholder:
    pass

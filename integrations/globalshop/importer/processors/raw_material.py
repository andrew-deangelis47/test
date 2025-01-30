from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import custom_table_patch
from baseintegration.utils.custom_table import ImportCustomTable
from paperless.client import PaperlessClient
from globalshop.part import Part, PartRecord


class MaterialImportProcessor(BaseImportProcessor):

    def _process(self, material_id: str):
        logger.info("Calling process method")
        material_dict = self.get_raw_material(material_id, self._importer.header_dict)
        if material_dict:
            headers = ImportCustomTable.assemble_custom_headers(material_dict)
            new_record = ImportCustomTable.generate_custom_header_nr(material_dict, headers)
            data = dict(row_data=new_record)
            client = PaperlessClient.get_instance()
            url = "suppliers/public/custom_tables/gss_materials/row"
            logger.info(f'calling custom table patch: {data}')
            custom_table_patch(client=client, data=data, url=url, identifier=material_id)

    def get_raw_material(self, material_id: str, header_dict) -> dict:
        mat: PartRecord = Part.get(material_id)
        logger.info(f"Material is : {mat}")

        row = {
            'material_id': mat.part.strip(),
            'mat_ext_desc': mat.extra_description,
            'mat_desc': mat.description,
            'mat_qty_onhand': mat.qty_last_onhand,
            'mat_net_onhand': mat.qty_last_onhand,
            'mat_rate': mat.amt_cost,
            'mat_alt_rate': mat.amt_alt_cost,
            'mat_cost_date': mat.cost_date,
            'mat_um_inventory': mat.um_inventory,
            'product_code': mat.product_line
        }

        for key, value in row.items():
            if key in header_dict:
                header_dict[key] = value
        return header_dict

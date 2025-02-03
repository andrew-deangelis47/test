from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.custom_table import ImportCustomTable
from baseintegration.datamigration import logger
from baseintegration.utils import custom_table_patch
from paperless.client import PaperlessClient
import ast


class MaterialImportProcessor(BaseImportProcessor):

    def _process(self, material_dict: str):  # noqa: C901
        material_dict = ast.literal_eval(material_dict)
        if "Family" not in material_dict or material_dict["Family"] is None or material_dict["Family"] == "":
            logger.info(f"Not bringing over {material_dict.get('ItemNumber')} because family is not populated")
            return
        if material_dict.get("ItemNumber") is None:
            logger.info("No item number, quitting early")
            return
        base_dict = self._importer.header_dict.copy()
        dict_to_upload = self.get_raw_material(material_dict, base_dict)
        if dict_to_upload:
            headers = ImportCustomTable.assemble_custom_headers(dict_to_upload)
            new_record = ImportCustomTable.generate_custom_header_nr(dict_to_upload, headers)
            data = dict(row_data=new_record)
            client = PaperlessClient.get_instance()
            url = f"suppliers/public/custom_tables/{self._importer.table_name}/row"
            custom_table_patch(client=client, data=data, url=url, identifier=material_dict.get("ItemNumber"))

    def get_raw_material(self, material_dict: dict, base_dict: dict):  # noqa: C901
        base_dict["price_code"] = material_dict.get("PriceCode")
        base_dict["item_number"] = material_dict.get("ItemNumber")
        base_dict["item_description"] = material_dict.get("ItemDescription")
        base_dict["Family"] = material_dict.get("Family")
        base_dict["Shape"] = material_dict.get("Shape")
        base_dict["image_url"] = material_dict.get("ImageUrl")
        base_dict["UoM"] = material_dict.get("UOM")
        base_dict["Cost"] = material_dict.get("Cost")
        if base_dict["Shape"] == "Sheet" or base_dict["Shape"] == "Plate":
            try:
                thickness = base_dict["item_description"].split(" ")[0].split("x")[0]
                if "MM" in thickness:
                    base_dict["Thickness"] = float(thickness.split("MM")[0]) / 25.4
                else:
                    base_dict["Thickness"] = float(thickness)
                base_dict["Width"] = float(base_dict["item_description"].split(" ")[0].split("x")[1])
                base_dict["Length"] = float(base_dict["item_description"].split(" ")[0].split("x")[2])
            except Exception:
                pass
        elif base_dict["Shape"] == "Rod":
            try:
                base_dict["Diameter"] = base_dict["item_description"].split(" ")[0]
            except:
                pass
        return base_dict

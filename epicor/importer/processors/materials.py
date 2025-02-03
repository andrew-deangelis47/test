from copy import deepcopy
from typing import List
from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.custom_table import ImportCustomTable
from epicor.part import MaterialPart as EpicorMaterialHelper
# Use a module-level variable to make sure this behavior only happens the first time the processor runs (per
# instantiation of the class). This is a way of saving redundant API calls
from epicor.api_models.paperless_custom_tables import MaterialCustomTableFormat
from epicor.client import EpicorClient
import datetime

from epicor.utils import get_epicor_part_cost_model


class EpicorBulkRawMaterialImportProcessor(BaseImportProcessor):
    # returning bool is purely for unit testing purposes, rather than error handling
    def _process(self, component_ids: List[str]) -> bool:
        materials: List[dict] = []
        for component_id in component_ids:
            try:
                logger.info(f"Processing material {component_id}")
                epicor_component: dict = EpicorMaterialHelper.get_part_by_part_num(component_id)
            except Exception as e:
                logger.info(e)
                logger.info("Material not being processed from Epicor")
                continue
            if str(epicor_component.get("InActive")).lower() == "true" or str(epicor_component.get("Inactive")).lower() == "true":
                logger.info(f"Got inactive part for {epicor_component.get('PartNum', None)}")
                continue
            new_table_row: MaterialCustomTableFormat = self.set_table_row_attributes(epicor_component)
            row_dict = self.remove_table_name(new_table_row.__dict__)
            materials.append(row_dict)
            if self._importer.erp_config.should_update_null_dates:
                self.update_null_updated_on_date(epicor_component)
        result: dict = ImportCustomTable.upload_records(
            identifier=f'epicor-material-bulk-upload-count-{len(materials)}',
            table_name=self._importer._paperless_table_model._custom_table_name,
            records=materials)
        return len(result["failures"]) == 0

    def remove_table_name(self, table_data: dict):
        try:
            del table_data["_custom_table_name"]
        except Exception:
            return table_data
        return table_data

    def set_table_row_attributes(self, epicor_part: dict) -> MaterialCustomTableFormat:
        paperless_table: MaterialCustomTableFormat = deepcopy(self._importer._paperless_table_model)
        paperless_table.part_num = self.get_epicor_part_num(epicor_part)
        # Get any related records using the part number and separate endpoints:
        epicor_part_cost_model: dict = self.get_epicor_part_cost_model(paperless_table.part_num)

        # Set all atrributes individually so that the individual methods can be overwritten
        paperless_table.part_description = self.get_epicor_part_description(epicor_part)
        paperless_table.class_id = self.get_epicor_part_class_id(epicor_part)
        paperless_table.type_code = self.get_epicor_part_type_code(epicor_part)
        paperless_table.non_stock = self.get_epicor_part_non_stock(epicor_part)
        paperless_table.prod_code = self.get_epicor_part_prod_code(epicor_part)
        paperless_table.pum = self.get_epicor_part_pum(epicor_part)
        paperless_table.ium = self.get_epicor_part_ium(epicor_part)
        paperless_table.avg_cost = self.get_epicor_part_avg_cost(epicor_part_cost_model)
        paperless_table.last_cost = self.get_epicor_part_last_cost(epicor_part_cost_model)
        return paperless_table

    def get_epicor_part_num(self, epicor_part: dict):
        return epicor_part.get("PartNum", None)

    def get_epicor_part_description(self, epicor_part: dict):
        return epicor_part.get("PartDescription", "No description")

    def get_epicor_part_class_id(self, epicor_part: dict):
        return epicor_part.get("ClassID", None)

    def get_epicor_part_type_code(self, epicor_part: dict):
        return epicor_part.get("TypeCode", None)

    def get_epicor_part_non_stock(self, epicor_part: dict):
        return bool(epicor_part.get("NonStock", True))

    def get_epicor_part_prod_code(self, epicor_part: dict):
        return epicor_part.get("ProdCode", "None")

    def get_epicor_part_pum(self, epicor_part: dict):
        return epicor_part.get("PUM", None)

    def get_epicor_part_ium(self, epicor_part: dict):
        return epicor_part.get("IUM", None)

    def get_epicor_part_cost_model(self, component_id: str, epicor_client: EpicorClient = None) -> dict:
        return get_epicor_part_cost_model(component_id, epicor_client)

    def get_epicor_part_avg_cost(self, epicor_part_cost_component: dict):
        padding_format = '{:.4f}'  # paperless api expects 4 max padding for decimal
        avg_cost_value: float = epicor_part_cost_component["AvgTotalCost"]
        avg_cost_value: str = padding_format.format(avg_cost_value)
        return avg_cost_value

    def get_epicor_part_last_cost(self, epicor_part_cost_component: dict):
        padding_format = '{:.4f}'  # paperless api expects 4 max padding for decimal
        last_cost_value: float = epicor_part_cost_component["LastTotalCost"]
        last_cost_value: str = padding_format.format(last_cost_value)
        return last_cost_value

    def update_null_updated_on_date(self, epicor_component: dict):
        """
        If config option is enabled, update legacy records ChangedOn date with the current date and time.
        (Legacy records are missing dates and therefore we cannot track changes without adding a last processed date).
        """
        updated_on = epicor_component.get("ChangedOn", None)
        part_num = epicor_component.get("PartNum", None)
        if updated_on is None or updated_on == "":
            patch_data: dict = {"ChangedOn": f"{str(datetime.datetime.now()).replace(' ', 'T')}Z"}
            url = f"Erp.BO.PartSvc/Parts('{self._importer.erp_config.company_name}','{part_num}')"
            client: EpicorClient = EpicorClient.get_instance()
            client.patch_resource(url, patch_data)


class EpicorRawMaterialImportProcessor(EpicorBulkRawMaterialImportProcessor):
    def _process(self, component_id: str) -> bool:
        return super()._process([component_id])


class EpicorMaterialBulkPlaceholder:
    pass

from paperless.client import PaperlessClient

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import custom_table_patch

from acumatica.api_models.acumatica_models import StockItem
from acumatica.api_models.paperless_custom_tables import MaterialCustomTableFormat


class AcumaticaRawMaterialImportProcessor(BaseImportProcessor):

    @staticmethod
    def format_as_row(raw_material: StockItem):
        data = dict(raw_material_id=raw_material.InventoryID,
                    base_price=raw_material.CurySpecificPrice,
                    description=raw_material.Description,
                    last_cost=raw_material.LastCost,
                    average_cost=raw_material.AverageCost,
                    last_modified=raw_material.LastModified)
        return data

    def _process(self, raw_material_string: str) -> bool:
        logger.info(f'Processing material {raw_material_string}')
        filters = {"InventoryID": raw_material_string}
        raw_material: StockItem = StockItem.get_first(filters=filters)
        raw_material_row = self.format_as_row(raw_material=raw_material)

        table_model = MaterialCustomTableFormat
        # TODO parent class should probably just do this
        id_name: str = table_model._primary_key
        table_name: str = table_model._custom_table_name
        url = f"suppliers/public/custom_tables/{table_name}/row"
        paperless_client: PaperlessClient = PaperlessClient.get_instance()
        custom_table_patch(client=paperless_client, data=dict(row_data=raw_material_row), url=url, identifier=id_name)
        return True

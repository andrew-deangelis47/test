from paperless.client import PaperlessClient

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import custom_table_patch

from acumatica.api_models.acumatica_models import NonStockItem
from acumatica.api_models.paperless_custom_tables import OutsideServiceCustomTableFormat


class AcumaticaOutsideServiceImportProcessor(BaseImportProcessor):

    @staticmethod
    def format_as_row(non_stock_item: NonStockItem, vendor_detail: dict):
        data = dict(
            osv_id=vendor_detail.get('id'),
            vendor_id=vendor_detail.get('VendorID', {}).get('value', 'N/A'),  # TODO
            vendor_name=vendor_detail.get('VendorName', 'N/A').get('value', 'N/A'),
            inventory_id=non_stock_item.InventoryID,
            description=non_stock_item.Description,
        )
        return data

    def _process(self, non_stock_item_id: str):
        logger.info(f'Processing Non Stock Item {non_stock_item_id}')
        table_model = OutsideServiceCustomTableFormat
        non_stock_item: NonStockItem = NonStockItem.get(id=non_stock_item_id)
        if not non_stock_item:
            return

        vendor_details = non_stock_item.VendorDetails
        if not vendor_details:
            return

        for vendor_dict in vendor_details:
            osv_row = self.format_as_row(non_stock_item=non_stock_item, vendor_detail=vendor_dict)
            # TODO parent class should probably just do this
            id_name: str = table_model._primary_key
            table_name: str = table_model._custom_table_name
            url = f"suppliers/public/custom_tables/{table_name}/row"
            paperless_client: PaperlessClient = PaperlessClient.get_instance()
            custom_table_patch(client=paperless_client, data=dict(row_data=osv_row), url=url, identifier=id_name)

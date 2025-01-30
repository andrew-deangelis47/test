from typing import List
from mietrak_pro.importer.utils import MieTrakProCustomTableImportProcessor
from mietrak_pro.models import Item, Itemcatalogcategory, Purchaseorderline
from baseintegration.utils import safe_get
from copy import deepcopy
from baseintegration.utils.custom_table import ImportCustomTable
from mietrak_pro.models.paperless_custom_tables import PurchaseOrderLineCustomTableFormat
from baseintegration.utils import logger


class MaterialImportProcessor(MieTrakProCustomTableImportProcessor):
    def _get_row_data(self, entity_id: int) -> dict:
        material: Item = Item.objects.filter(itempk=entity_id).first()
        if not material:
            raise Exception(f"Was not able to import material {entity_id} as it could not be found in the Item table")
        row = {
            "ItemPK": material.itempk,
            "PartNumber": material.partnumber,
            "Description": material.description,
            "StockLength": material.stocklength,
            "StockWidth": material.stockwidth,
            "Thickness": material.thickness,
            "Weight": material.weight,
            "WeightFactor": material.weightfactor,
            "SquareFootPerPound": material.squarefootperpound
        }
        if material.iteminventoryfk:
            row.update({
                "LastCost": material.iteminventoryfk.lastcost
            })
        if self._importer.erp_config.should_import_category:
            category = Itemcatalogcategory.objects.filter(itemfk=entity_id).first()
            row.update({
                "Category": safe_get(category, 'catalogcategoryfk.name')
            })
        if self._importer.erp_config.should_import_leadtime:
            row.update({"Leadtime": material.leadtime})
        if self._importer.erp_config.should_import_vendor:
            vendor = material.partyfk
            vendor_name = safe_get(vendor, 'name')
            row.update({"Vendor": vendor_name})

        if self._importer.erp_config.should_import_po_history:
            self.upload_po_history(entity_id)
        return row

    @classmethod
    def upload_po_history(self, entity_id):
        po_lines: List[dict] = []
        lines = Purchaseorderline.objects.filter(itemfk=entity_id).order_by("-createdate")[:10]
        for po_line in lines:
            new_table_row = self.get_po_line_table_row(po_line)
            row_data = self.remove_table_name(new_table_row.__dict__)
            po_lines.append(row_data)
        po_line_result: dict = ImportCustomTable.upload_records(
            identifier=f'mietrak-po-line-bulk-upload-count-{len(po_lines)}',
            table_name="purchase_order_line_custom_table",
            records=po_lines)
        if po_line_result['failures']:
            logger.error(po_line_result['failures'])

    @classmethod
    def remove_table_name(self, table_data):
        try:
            del table_data["_custom_table_name"]
        except Exception:
            return table_data
        return table_data

    @classmethod
    def get_po_line_table_row(self, po_line: Purchaseorderline):
        paperless_table = deepcopy(PurchaseOrderLineCustomTableFormat())
        paperless_table.purchaseorderlinepk = po_line.purchaseorderlinepk
        paperless_table.purchaseorderfk = po_line.purchaseorderfk.purchaseorderpk
        paperless_table.itemfk = po_line.itemfk.itempk
        paperless_table.unitofmeasurecode = po_line.unitofmeasuresetfk.code
        paperless_table.quantity = float(po_line.quantity)
        paperless_table.price = float(po_line.price)
        paperless_table.createdate = str(po_line.createdate)
        paperless_table.closeddate = str(po_line.closeddate)
        return paperless_table


class MieTrakProMaterialBulkImportProcessor(MaterialImportProcessor):
    def _process(self, entity_ids: List[int]):
        self.update_custom_table(entity_ids=entity_ids)


class BulkMaterialImportPlaceholder:
    pass

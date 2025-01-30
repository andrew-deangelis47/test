from mietrak_pro.importer.utils import MieTrakProCustomTableImportProcessor
from mietrak_pro.models import Item, Itemcatalogcategory
from baseintegration.utils import safe_get


class OutsideServiceImportProcessor(MieTrakProCustomTableImportProcessor):
    def _get_row_data(self, entity_id: int) -> dict:
        service: Item = Item.objects.filter(itempk=entity_id).first()
        if not service:
            raise Exception(f"Was not able to import outside process {entity_id} as it could not be found in the Item "
                            f"table")
        row = {
            "ItemPK": service.itempk,
            "PartNumber": service.partnumber,
            "VendorPartNumber": service.vendorpartnumber,
            "Description": service.description
        }
        if service.partyfk:
            row.update({
                "Vendor": service.partyfk.name,
                "PartyPK": service.partyfk.partypk
            })
        if self._importer.erp_config.should_import_category:
            category = Itemcatalogcategory.objects.filter(itemfk=entity_id).first()
            row.update({
                "Category": safe_get(category, 'catalogcategoryfk.name')
            })
        if self._importer.erp_config.should_import_leadtime:
            row.update({"Leadtime": service.leadtime})

        if self._importer.erp_config.should_import_costs:
            for i in range(1, 11):
                row.update({f'price{i}': getattr(service, f'price{i}')})
                row.update({f'quantity{i}': getattr(service, f'quantity{i}')})
                row.update({f'sellprice{i}': getattr(service, f'sellprice{i}')})
        return row

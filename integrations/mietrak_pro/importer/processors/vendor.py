from mietrak_pro.importer.utils import MieTrakProCustomTableImportProcessor
from mietrak_pro.models import Party


class VendorImportProcessor(MieTrakProCustomTableImportProcessor):
    def _get_row_data(self, entity_id: int) -> dict:
        vendor: Party = Party.objects.filter(partypk=entity_id).first()
        if not vendor:
            raise Exception(f"Was not able to import vendor {entity_id} as it could not be found in the Party table")
        row = {
            "PartyPK": vendor.partypk,
            "Name": vendor.name,
            "ShortName": vendor.shortname,
            "Phone": vendor.phone,
            "Fax": vendor.fax,
            "Email": vendor.email
        }
        if vendor.shipviafk:
            row.update({
                "ShipVia": vendor.shipviafk.description,
                "ShipViaPK": vendor.shipviafk.shipviapk
            })
        return row

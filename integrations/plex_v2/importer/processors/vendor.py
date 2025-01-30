from typing import List
from baseintegration.utils import custom_table_patch
from paperless.client import PaperlessClient
from plex_v2.objects.supplier import Supplier
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex_v2.factories.paperless.vendor_custom_table_row import VendorCustomTableRowFactory
from plex_v2.importer.processors.base import PlexImportProcessor


class VendorBulkImportProcessor(PlexImportProcessor):
    _fallback_country_alpha_3 = 'USA'

    def _process(self, supplier_ids: List[str], vendor_custom_table_row_factory: VendorCustomTableRowFactory):
        client = PaperlessClient.get_instance()
        url = f"suppliers/public/custom_tables/{self._importer._paperless_table_model._custom_table_name}/row"

        for supplier_id in supplier_ids:

            # 1) get the supplier
            try:
                supplier: Supplier = Supplier.search(code=supplier_id)[0]
            except Exception:
                raise CancelledIntegrationActionException(f'Could not find supplier with id "{supplier_id}"')
            except IndexError:
                raise CancelledIntegrationActionException(f'Could not find supplier with id "{supplier_id}"')

            # 2) convert to custom table row and update
            row = vendor_custom_table_row_factory.to_custom_table_row(supplier)

            try:
                custom_table_patch(client=client, data=dict(row_data=row), url=url, identifier=f'Supplier {supplier.name}')
            except Exception as e:
                raise CancelledIntegrationActionException(e)

        return True


class VendorImportProcessor(VendorBulkImportProcessor):
    def _process(self, vendor_id: str, vendor_custom_table_row_factory: VendorCustomTableRowFactory) -> bool:
        return super()._process([vendor_id], vendor_custom_table_row_factory)


class VendorBulkPlaceholder:
    pass

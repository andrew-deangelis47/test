from paperless.client import PaperlessClient
from typing import List, Union
from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import custom_table_patch
from sage.exceptions import SageInvalidResourceRequestedException, SageInvalidResponsePayloadException
from sage.models.paperless_custom_tables.vendors_table import VendorsTable
from sage.sage_api.client import SageImportClient
from sage.sage_api.filter_generation.vendor_filter_generator import VendorFilterGenerator
from sage.models.sage_models.vendor import SupplierFullEntity


def _get_vendor(client: SageImportClient, supplier_id: str) -> Union[SupplierFullEntity, bool]:
    """
    - calls the sage client to get the specified supplier (vendor)
    - returns the sage vendor object, or False if it does not find one
    """
    try:
        sage_supplier = client.get_resource(
            SupplierFullEntity,
            VendorFilterGenerator.get_filter_by_id(supplier_id),
            False
        )
    except (SageInvalidResourceRequestedException, SageInvalidResponsePayloadException) as ex:
        logger.error(ex)
        return False

    # check that we actually got back some data
    if sage_supplier is None:
        logger.error('No supplier found with id ' + supplier_id)
        return False

    # if everything worked return the raw material
    return sage_supplier


class SageBulkVendorImportProcessor(BaseImportProcessor):

    @staticmethod
    def format_as_row(supplier_full_entity: SupplierFullEntity):
        data = {
            'vendor_id': supplier_full_entity.supplier.vendor_id,
            'name': supplier_full_entity.supplier.name,
        }
        return data

    def _process(self, suppliers_ids: List[str]) -> bool:
        client = SageImportClient.get_instance()
        for supplier_id in suppliers_ids:

            # 1) get the vendor from the sage api and convert to custom table row
            vendor = _get_vendor(client, supplier_id)
            if not vendor:
                logger.error('Skipping supplier ' + supplier_id)
                continue

            # 2) Setup custom table information
            raw_vendor_row = self.format_as_row(vendor)
            table_model = VendorsTable
            table_model.vendor_id = raw_vendor_row['vendor_id']
            table_model.name = raw_vendor_row['name']
            id_name: str = table_model._primary_key
            table_name: str = table_model._custom_table_name

            # 3) Make the call to update the custom table with the raw material
            url = f"suppliers/public/custom_tables/{table_name}/row"
            paperless_client: PaperlessClient = PaperlessClient.get_instance()
            custom_table_patch(client=paperless_client, data=dict(row_data=raw_vendor_row), url=url, identifier=id_name)

        return True


class SageVendorImportProcessor(SageBulkVendorImportProcessor):
    def _process(self, component_id: str) -> bool:
        logger.info(f"the component id {component_id}")
        return super()._process([component_id])


class SageVendorBulkPlaceholder:
    pass

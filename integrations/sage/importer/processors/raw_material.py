from paperless.client import PaperlessClient
from typing import List, Union
from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import custom_table_patch
from sage.models.paperless_custom_tables.raw_materials import RawMaterial as PaperlessRawMaterial
from sage.sage_api.client import SageImportClient
from sage.sage_api.filter_generation.part_filter_generator import PartFilterGenerator
from sage.exceptions import SageInvalidResourceRequestedException, SageInvalidResponsePayloadException
from sage.models.sage_models.part import PartFullEntity


def _get_raw_material(client: SageImportClient, material_id: str) -> Union[PaperlessRawMaterial, bool]:
    """
    - calls the sage client to get the specified raw material
    - returns the paperless raw material object, or False if it does not find one
    """
    try:
        sage_purchased_component = client.get_resource(
            PartFullEntity,
            PartFilterGenerator.get_filter_by_id(material_id),
            False
        )
    except (SageInvalidResourceRequestedException, SageInvalidResponsePayloadException) as ex:
        logger.error(ex)
        return False

    # check that we actually got back some data
    if sage_purchased_component is None:
        logger.error('No raw material found with id ' + material_id)
        return False

    # if everything worked return the raw material
    return sage_purchased_component


class SageBulkRawMaterialImportProcessor(BaseImportProcessor):

    @staticmethod
    def format_as_row(raw_material: PartFullEntity):
        data = {
            'part_num': raw_material.product.product_code,
            'piece_price': raw_material.prod_site_totals.purchase_base_price,
            'class_id': raw_material.product.product_category,
            'description': raw_material.product.description
        }
        return data

    def _process(self, raw_material_ids: List[str]) -> bool:
        client = SageImportClient.get_instance()
        for raw_material_id in raw_material_ids:

            # 1) get the raw material from the sage api
            raw_material = _get_raw_material(client, raw_material_id)
            if not raw_material:
                logger.error('Skipping raw material ' + raw_material_id)
                continue

            # 2) Setup custom table information
            raw_material_row = self.format_as_row(raw_material=raw_material)
            table_model = PaperlessRawMaterial
            table_model.part_num = raw_material_row['part_num']
            table_model.piece_price = raw_material_row['piece_price']
            table_name: str = table_model._custom_table_name

            # 3) Make the call to update the custom table with the raw material
            url = f"suppliers/public/custom_tables/{table_name}/row"
            paperless_client: PaperlessClient = PaperlessClient.get_instance()
            custom_table_patch(client=paperless_client, data=dict(row_data=raw_material_row), url=url,
                               identifier=raw_material.product.product_code)

        return True


class SageRawMaterialImportProcessor(SageBulkRawMaterialImportProcessor):
    def _process(self, component_id: str) -> bool:
        return super()._process([component_id])


class SageMaterialBulkPlaceholder:
    pass

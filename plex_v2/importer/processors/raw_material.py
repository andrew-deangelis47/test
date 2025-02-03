from typing import List
from plex_v2.objects.part import Part
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from baseintegration.datamigration import logger
from plex_v2.utils.material_pricing_helper import MaterialPricingHelper
from plex_v2.objects.raw_material_attribute import RawMaterialAttribute
from plex_v2.factories.paperless.raw_material_attributes_factory import RawMaterialAttributesFactory
from plex_v2.factories.paperless.raw_material_custom_table_row import RawMaterialCustomTableRowFactory
from baseintegration.utils.custom_table import ImportCustomTable
from plex_v2.importer.processors.base import PlexImportProcessor
import time


class RawMaterialBulkImportProcessor(PlexImportProcessor):

    def _process(self, material_ids: List[int], raw_material_custom_table_row_factory: RawMaterialCustomTableRowFactory, raw_material_attributes_factory: RawMaterialAttributesFactory):

        material_rows: List[dict] = []
        for material_id in material_ids:

            # 0) get the material object(s)
            logger.info(f'Processing material {material_id}')
            materials: Part = Part.find_part(number=material_id)

            if len(materials) == 0:
                raise CancelledIntegrationActionException(f'Part not found: "{material_id}". Check for special characters in the part number within Plex')

            material: Part
            for material in materials:

                # 1) make sure status is valid
                if material.status not in self.config.part_statuses_active:
                    logger.info(f'Part {material.number} rev {material.revision} is not active (status is "{material.status}", skipping')
                    continue

                # 2) get all configured attributes
                attributes: List[RawMaterialAttribute] = raw_material_attributes_factory.get_raw_material_attributes(material)

                # 3) convert to raw material row and update table
                row = raw_material_custom_table_row_factory.to_custom_table_row(material, attributes)
                material_rows.append(row)

            # if we are importing material pricing, or inventory levels, we need to import in batches - the datasources we use get overwhelmed if not
            if (self.config.should_import_material_pricing or self.config.should_import_material_inventory) and len(material_rows) > 49:
                self._bulk_update_materials(material_rows)
                time.sleep(20)
                material_rows = []

        # if we are not importing pricing we do the whole upload at the end
        return self._bulk_update_materials(material_rows)

    def _bulk_update_materials(self, material_rows: List[dict]) -> bool:
        logger.info(f"Attemping to update/insert {len(material_rows)} materials: {', '.join([material['Number'] for material in material_rows])}")
        result = ImportCustomTable.upload_records(
            identifier=f'plex-material-bulk-upload-count-{len(material_rows)}',
            table_name=self._importer._paperless_table_model._custom_table_name,
            records=material_rows)
        if len(result['failures']) > 0:
            logger.info('FAILED TO UPDATE RAW MATERIALS TABLE')
            logger.info(result['failures'])
            return False

        return True


class RawMaterialImportProcessor(RawMaterialBulkImportProcessor):

    def _process(self, material_id: str, material_pricing_helper: MaterialPricingHelper,
                 raw_material_custom_table_row_factory: RawMaterialCustomTableRowFactory, raw_material_attributes_factory: RawMaterialAttributesFactory) -> bool:
        return super()._process([material_id], material_pricing_helper, raw_material_custom_table_row_factory, raw_material_attributes_factory)


class RawMaterialBulkPlaceholder:
    pass

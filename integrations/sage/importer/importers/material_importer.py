from baseintegration.importer.material_importer import MaterialImporter
from sage.importer.importer import SageImporter
from sage.models.paperless_custom_tables.raw_materials import RawMaterial
from sage.importer.listeners.raw_material import SageRawMaterialImportListener
from paperless.objects.components import Material
from sage.importer.processors.raw_material import SageRawMaterialImportProcessor, SageBulkRawMaterialImportProcessor, SageMaterialBulkPlaceholder
from baseintegration.datamigration import logger
from typing import List
from sage.importer.configuration import SageRawMaterialConfig


class SageMaterialImporter(MaterialImporter, SageImporter):
    _paperless_table_model = RawMaterial()

    def _register_listener(self):
        self.listener = SageRawMaterialImportListener(self._integration)

    def _register_default_processors(self):
        self.register_processor(Material, SageRawMaterialImportProcessor)
        # change model, select the right processor for it
        self.register_processor(SageMaterialBulkPlaceholder, SageBulkRawMaterialImportProcessor)
        logger.info('Registered raw material processor.')

    def _process_material(self, material_id: str):  # noqa: C901
        logger.info(f"Material id is {str(material_id)}")
        with self.process_resource(Material, material_id):
            logger.info(f"Processed Material id: {material_id}")

    def _bulk_process_material(self, material_ids: List[str]):  # noqa: C901
        with self.process_resource(SageMaterialBulkPlaceholder, material_ids) as success:
            logger.info(f"Bulk processed {len(material_ids)} raw materials")
            return success

    def _setup_erp_config(self):
        self.erp_config = SageRawMaterialConfig(self._integration.config_yaml)

    def check_custom_table_exists(self):
        self.add_or_remove_custom_table_attributes()
        self._paperless_table_model.check_custom_header_custom_table_exists()

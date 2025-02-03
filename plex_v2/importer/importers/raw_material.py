from baseintegration.datamigration import logger
from baseintegration.importer.material_importer import MaterialImporter
from plex_v2.configuration import ERPConfigFactory
from plex_v2.importer.listeners import PLEXRawMaterialListener
from paperless.objects.components import Material
from plex_v2.importer.processors import RawMaterialBulkPlaceholder, RawMaterialBulkImportProcessor, RawMaterialImportProcessor
from typing import List
from plex_v2.objects.raw_material_custom_table import RawMaterialCustomTable
from plex_v2.factories.paperless import RawMaterialCustomTableRowFactory
from plex_v2.utils.material_pricing_helper import MaterialPricingHelper
from plex_v2.utils.import_utils import ImportUtils
from baseintegration.utils.operations import OperationUtils
from plex_v2.factories.paperless.raw_material_attributes_factory import RawMaterialAttributesFactory
import os
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
import yaml
from baseintegration.integration.erp_error_message_converter import ERPErrorMessageConverter


class PLEXRawMaterialImporter(MaterialImporter):

    def _setup_erp_config(self):
        # 1) setup config, client, and custom table model
        self.erp_config, self.plex_client = ERPConfigFactory.create_importer_config(self._integration, 'materials')

        # setup util class
        self._setup_util_classes()

        # setup factories
        self._setup_factories()

        # setup the custom table model
        self._paperless_table_model = RawMaterialCustomTable(self.erp_config, self.utils)

        self._setup_error_message_converter()

    def _setup_util_classes(self):
        print(self.erp_config.raw_material_part_attributes)
        operation_utils: OperationUtils = OperationUtils()
        self.utils: ImportUtils = ImportUtils(self.erp_config, operation_utils)

    def _setup_factories(self):
        material_pricing_helper: MaterialPricingHelper = MaterialPricingHelper(self.utils, self.erp_config)
        self.raw_material_custom_table_row_factory = RawMaterialCustomTableRowFactory(self.erp_config, self.utils, material_pricing_helper)
        self.raw_material_attributes_factory: RawMaterialAttributesFactory = RawMaterialAttributesFactory(self.erp_config, self.utils)

    def _register_default_processors(self):
        self.register_processor(Material, RawMaterialImportProcessor)
        self.register_processor(RawMaterialBulkPlaceholder, RawMaterialBulkImportProcessor)

    def _register_listener(self):
        self.listener = PLEXRawMaterialListener(self._integration, self.erp_config)

    def _process_material(self, material_id: str):
        with self.process_resource(Material, material_id, self.raw_material_custom_table_row_factory, self.raw_material_attributes_factory) as result:
            return result

    def _bulk_process_material(self, material_ids: List[str]):  # noqa: C901
        with self.process_resource(RawMaterialBulkPlaceholder, material_ids, self.raw_material_custom_table_row_factory, self.raw_material_attributes_factory) as success:
            logger.info(f"Bulk processed {len(material_ids)} raw materials")
            return success

    def check_custom_table_exists(self):
        self.add_or_remove_custom_table_attributes()
        self._paperless_table_model.check_custom_header_custom_table_exists()

    def add_or_remove_custom_table_attributes(self):
        """
        - Override this class and use the setattr() or delattr() functions to add or remove attributes to or from the
        custom table format.
        - Examples:
            - setattr(self._paperless_table_model, "new_atrribute", "xyz123")
            - delattr(self._paperless_table_model, "part_num")
        NOTE: You will also need to override the set_table_row_attributes() function in the "materials" imports processor
        to correspond with your updated class attributes
        """
        pass

    def _setup_error_message_converter(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), "../../erp_error_message_mapping.yaml")) as file:
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                config_yaml = yaml.load(file, Loader=yaml.FullLoader)
                self.error_message_converter = ERPErrorMessageConverter(config_yaml.get("Mapping"))
        except Exception as e:
            logger.info(str(e))
            raise CancelledIntegrationActionException('Could not read from error message mapping. Please contact support.')

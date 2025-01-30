from baseintegration.integration import Integration
# Set up a basic logger just in case something tries to use the logger before
# configure_logging() is run
import logging
from paperless.objects.integration_actions import IntegrationAction
from baseintegration.integration.erp_error_message_converter import ERPErrorMessageConverter
import os
import yaml

logger = logging.getLogger('paperless')
logger.setLevel(logging.DEBUG)
logging_configured = False


class BaseDataMigration:
    """
    This class is overriden by BaseImporter and BaseExporter and stores
    functionality consistent between both importers and exporters. It also
    stores the integration scheduler as an instance variable to be accessed
    later
    """

    erp_name = None
    erp_config = None
    erp_error_message_converter: ERPErrorMessageConverter

    def __init__(self, integration):
        self._integration: Integration = integration
        self._setup_erp_config()
        self._setup_erp_client()
        self._registered_processors = {}
        self._register_default_processors()
        self._register_custom_processors()
        self.success_message = None
        self._setup_error_message_converter()

    def _setup_error_message_converter(self):
        try:
            logger.info('Attempting to setup error message converter')
            mapping_file_location = f'../../{self._integration.config_yaml["Paperless"]["dir_to_preserve"]}/erp_error_message_mapping.yaml'
            with open(os.path.join(os.path.dirname(__file__), mapping_file_location)) as file:
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                config_yaml = yaml.load(file, Loader=yaml.FullLoader)
                self.error_message_converter = ERPErrorMessageConverter(config_yaml.get("Mapping"))
        except Exception as e:
            logger.warning(f'Cannot read from error message mapping file. Errors will not be converted gracefully. Error is {e}')
            self.erp_error_message_converter = None

    def _setup_erp_config(self):
        """
        This creates a configuration object that is referenced by this
        Integration object and made available to processors. Does nothing
        unless overridden.
        """

        # If the erp_config object isn't set with defaults then create a
        pass

    def _setup_erp_client(self):
        """
        Setup the ERP client if different from the config
        """
        pass

    def _register_default_processors(self):
        """
        This should be overridden on the base ERP processors to register the
        default processors. Then the implementation only needs to
        add/override/remove a few additional registrations.
        """
        pass

    def _register_custom_processors(self):
        """
        This should allow users to override specific processes within each
        exporter / importer
        """
        pass

    def create_integration_action(self, action_type: str, entity_id: str) -> IntegrationAction:
        ia = IntegrationAction(type=action_type, entity_id=str(entity_id))
        ia.create(managed_integration_uuid=self._integration.managed_integration_uuid)
        # bug where you can't update the IA but have to go get it
        return IntegrationAction.get(ia.uuid)

from baseintegration.datamigration import logger
from baseintegration.importer.account_importer import AccountImporter
from plex_v2.configuration import ERPConfigFactory
from plex_v2.objects.customer import Customer
from plex_v2.importer.processors import AccountImportProcessor
from plex_v2.importer.listeners import PLEXAccountListener
from plex_v2.utils.import_utils import ImportUtils
from plex_v2.factories.paperless import AccountFactory, ContactFactory
from baseintegration.utils.operations import OperationUtils
import os
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
import yaml
from baseintegration.integration.erp_error_message_converter import ERPErrorMessageConverter
from plex_v2.factories.paperless.payment_terms_mapping_factory import PaymentTermsMappingFactory
from plex_v2.objects.payment_terms_mapping import PaymentTermsMappingList


class PLEXAccountImporter(AccountImporter):

    def _setup_erp_config(self):
        # 1) create config and client
        self.erp_config, self.plex_client = ERPConfigFactory.create_importer_config(self._integration, 'accounts')

        # 2) setup util classes
        self._setup_util_classes()

        # 3) setup factories
        self._setup_factories()

        # 4) if payment terms are configured lets grab those from the custom table
        self.payment_terms_mapping_list: PaymentTermsMappingList = None
        if self.erp_config.should_import_customer_terms:
            self.payment_terms_mapping_list = self.payment_terms_mapping_list_factory.get_payment_terms_mapping_list()

        # 5) setup the error message converter
        self._setup_error_message_converter()

    def _register_default_processors(self):
        self.register_processor(Customer, AccountImportProcessor)

    def _register_listener(self):
        self.listener = PLEXAccountListener(self._integration, self.erp_config)

    def _process_account(self, account_id: str):
        self._setup_erp_config()
        logger.info(f"Processing Account: {str(account_id)}")
        with self.process_resource(Customer, account_id, self.utils, self.account_factory, self.contact_factory, self.payment_terms_mapping_list) as result:
            return result

    def _setup_util_classes(self):
        operation_utils: OperationUtils = OperationUtils()
        self.utils = ImportUtils(self.erp_config, operation_utils)

    def _setup_factories(self):
        self.account_factory = AccountFactory(self.erp_config)
        self.contact_factory = ContactFactory(self.erp_config)
        self.payment_terms_mapping_list_factory: PaymentTermsMappingFactory = PaymentTermsMappingFactory(self.erp_config, self.utils)

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

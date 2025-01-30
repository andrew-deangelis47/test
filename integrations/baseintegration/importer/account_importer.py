from baseintegration.importer import BaseImporter
from baseintegration.exporter.exceptions import IntegrationNotImplementedError
from baseintegration.datamigration import logger
from baseintegration.integration import Integration


class AccountImporter(BaseImporter):
    """Imports accounts from ERP to Paperless. Should be overriden by an ERP specific importer.
    Requires an ERP specific listener with a "get_new" function"""

    def __init__(self, integration: Integration):
        super().__init__(integration)
        logger.info("Instantiated the account importer")

    def run(self, account_id: str = None):
        logger.info("Calling run for the AccountImporter")
        method_to_call = getattr(self, '_process_account')
        super().importer_run("accounts", method_to_call, "import_account", False, account_id)

    def _process_account(self, account_id: str):
        """
        This is the main driver of the whole integration process. This needs to be overridden by the base class
        :return: The success status of the order processing
        """
        logger.info("attempting to process account")
        raise IntegrationNotImplementedError(f"_process_account() is not implemented for {self.__class__.__name__}")

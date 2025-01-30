from baseintegration.datamigration import logger
from baseintegration.importer.account_importer import AccountImporter
from baseintegration.importer.material_importer import MaterialImporter
from visualestitrack.importer.processors.accounts import AccountImportProcessor
from visualestitrack.importer.processors.inventory import SyncInventory
from visualestitrack.importer.processors.material_types import \
    SyncMaterialTypes
from visualestitrack.models import Facilities, Inventory, Materialtype
from paperless.objects.customers import AccountList


class VisualEstiTrackAccountListener:
    def __init__(self, integration):
        self.identifier = "import_account"
        self._integration = integration

    @staticmethod
    def get_new(bulk=False):
        customers_query_set = Facilities.objects.all()
        customer_list = list(set(customers_query_set.values_list('estitrack_account_id', flat=True)))
        pp_account_list = AccountList.list()
        for account in pp_account_list:
            if account.erp_code is not None and account.erp_code in customer_list:
                customer_list = filter(lambda val: val != account.erp_code, customer_list)
            if isinstance(customer_list, filter):
                customer_list = []
        return customer_list


class VisualEstiTrackAccountImporter(AccountImporter):

    def _setup_erp_config(self):
        pass

    def _register_default_processors(self):
        self.register_processor(Facilities, AccountImportProcessor)

    def _register_listener(self):
        self.listener = VisualEstiTrackAccountListener(self._integration)

    def _process_account(self, account_id: str):
        self._setup_erp_config()
        logger.info("Processing: Facilities")
        with self.process_resource(Facilities, account_id) as result:
            return result


class VisualEstiTrackMaterialListener:
    def __init__(self, integration):
        self.identifier = "import_material"
        self._integration = integration

    def check_custom_table_exists(self):
        return True

    def get_new(self, bulk=False):
        return [
            '1']  # We are always syncing over the entire table from VET, Therefore we will not look for changes


class VisualEstiTrackMaterialImporter(MaterialImporter):

    def _setup_erp_config(self):
        pass

    def _register_default_processors(self):
        self.register_processor(Inventory, SyncInventory)
        self.register_processor(Materialtype, SyncMaterialTypes)

    def _register_listener(self):
        self.listener = VisualEstiTrackMaterialListener(self._integration)

    def _process_material(self, material_id: str):
        self._setup_erp_config()
        logger.info("Processing: Materialtype and Inventory")

        with self.process_resource(Materialtype):
            with self.process_resource(Inventory) as result2:
                return result2

    def check_custom_table_exists(self):
        return True

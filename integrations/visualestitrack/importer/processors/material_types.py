from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.custom_table import ImportCustomTable
from visualestitrack.models import Materialtype


class SyncMaterialTypes(BaseImportProcessor):

    def _process(self):
        return ImportCustomTable.import_from_django_model(Materialtype, 'Materialtype', True, True)

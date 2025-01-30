from dataclasses import dataclass
from baseintegration.importer import BaseImporter
from sage.sage_api.client import SageImportClient


@dataclass
class SageImporter(BaseImporter):
    def __init__(self, integration):
        super().__init__(integration)

    def _setup_erp_client(self):
        if not self._integration.test_mode:
            api_url = self._integration.secrets["Sage"]["base_url"]
            username = self._integration.secrets["Sage"]["username"]
            password = self._integration.secrets["Sage"]["password"]
            # Todo: This doesn't actually test if client is valid, its going to be a silent failure
            self.client = SageImportClient(base_url=api_url, username=username, password=password)
        else:
            self.client = SageImportClient(api_key="test", base_url="http://testapi.com", username="test", password="test")
        self._integration.api_client = self.client

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

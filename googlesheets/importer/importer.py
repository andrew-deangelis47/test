from baseintegration.datamigration import logger
from baseintegration.importer.material_importer import MaterialImporter
from baseintegration.utils.custom_table import ImportCustomTable
from googlesheets.importer.processors.material import MaterialImportProcessor
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account


class GoogleSheetsMaterialImportListener:

    def __init__(self, integration):
        self.identifier = "import_material"
        self._integration = integration

    def get_new(self, bulk=False):
        material_dict_list = []
        if not self._integration.test_mode:
            service = build('sheets', 'v4', credentials=self._integration.config["creds"])
            spreadsheet_id = self._integration.config_yaml["GoogleSheets"]["spreadsheet_id"]
            # Call the Sheets API
            sheets = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()["sheets"]

            for sheet in sheets:
                sheet_title = sheet["properties"]["title"]
                new_range = f"{sheet_title}!$A$1:$YY"
                result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                             range=new_range).execute()
                values = result.get('values', [])

                # make each row into a dictionary
                for i, row in enumerate(values):
                    if i == 0:
                        if "Family" not in row:
                            break
                    else:
                        row_dict = {}
                        for i, key in enumerate(values[0]):
                            try:
                                row_dict[key] = row[i]
                            except:
                                continue
                        material_dict_list.append(row_dict)
        else:
            material_dict_list.append({"PriceCode": "test", "Family": "test", "ItemNumber": "testing123", "ItemDescription": ".056x48x96 Black ABS Sheet", "Shape": "Sheet"})
            material_dict_list.append({"PriceCode": "test", "ItemNumber": "testing123", "ItemDescription": ".056x48x96 Black ABS Sheet", "Shape": "Sheet"})
            material_dict_list.append({"PriceCode": "test", "Family": "test", "ItemDescription": ".056x48x96 Black ABS Sheet", "Shape": "Sheet"})
        return material_dict_list


class GoogleSheetsMaterial:
    """This class exists so we can meet the processor model, no other reason"""


class GoogleSheetsMaterialImporter(MaterialImporter):

    def _register_default_processors(self):
        self.register_processor(GoogleSheetsMaterial, MaterialImportProcessor)

    def _setup_erp_config(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        if not self._integration.test_mode:
            self.table_name = "materials"
            if os.path.exists('token.json'):
                self._integration.config["creds"] = service_account.Credentials.from_service_account_file('token.json',
                                                                                                          scopes=SCOPES,
                                                                                                          subject="pparts@regalplastic.com")
            else:
                raise ValueError("Could not creds")
        else:
            self.table_name = "google_sheets_materials"

    def _register_listener(self):
        self.listener = GoogleSheetsMaterialImportListener(self._integration)

    def check_custom_table_exists(self):
        logger.info("We're creating a dictionary.")
        self.header_dict = {
            'price_code': "720",
            'item_number': "Blah",
            'image_url': "N/A",
            'item_description': "Description",
            'Thickness': 0.0,
            'Width': 0.0,
            'Length': 0.0,
            'Diameter': 0.0,
            'Cost': 0.0,
            'UoM': 'SHT',
            'Family': 'ABS',
            'Shape': 'Sheet'
        }
        return ImportCustomTable.check_custom_header_custom_table_exists(self.table_name, self.header_dict, "item_number")

    def _process_material(self, material_dict: dict):  # noqa: C901
        logger.info(f"Material dict is {str(material_dict)}")
        with self.process_resource(GoogleSheetsMaterial, material_dict):
            logger.info("Successfully processed!")

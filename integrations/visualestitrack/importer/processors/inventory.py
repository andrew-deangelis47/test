import csv
import requests

from paperless.client import PaperlessClient
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils.custom_table import ImportCustomTable
from baseintegration.datamigration import logger
from visualestitrack.models import Inventory


class SyncInventory(BaseImportProcessor):

    def _process(self):
        table_name = 'inventory'
        config, headers = ImportCustomTable.convert_datastructures(Inventory)
        data = ImportCustomTable.generate_table_data(Inventory, headers)
        if len(data) == 0:
            logger.info('No inventory data found in VET interim DB, skipping')
            return True
        ImportCustomTable.upload_custom_table(config, [], table_name, True)

        config_file_path = '/tmp/inventory_config.csv'
        data_file_path = '/tmp/inventory_data.csv'

        with open(config_file_path, 'w', newline='') as f:
            config_writer = csv.DictWriter(f, fieldnames=['column_name', 'value_type', 'is_for_unique_key'])
            config_writer.writeheader()
            for config_row in config:
                config_writer.writerow(config_row)

        with open(data_file_path, 'w', newline='') as f:
            header_names = []
            for pair in headers:
                header_names.append(pair[0])
            data_writer = csv.DictWriter(f, fieldnames=header_names)
            data_writer.writeheader()
            for data_row in data:
                data_writer.writerow(data_row)

        client: PaperlessClient = PaperlessClient.get_instance()
        headers = {'Authorization': 'API-Token {}'.format(client.access_token)}
        url = f'{client.base_url}/suppliers/public/custom_tables/{table_name}'
        with open(data_file_path, 'rb') as data_stream:
            with open(config_file_path, 'rb') as config_stream:
                return self.upload_retry(url, headers, config_stream, data_stream)
        return True

    def upload_retry(self, url: str, headers: list, config: str, data: str) -> bool:
        try:
            r = self.upload(url, headers, config, data)
            if int(r.status_code) >= 400:
                r = self.upload(url, headers, config, data)
                if int(r.status_code) >= 400:
                    logger.error(f'Upload Failed: Something went wrong while retrying uploading the inventory table. '
                                 f'Please check the custom table`s integrity. http code {r.status_code} - {r.text}')
                    return False
                return True
            return True
        except Exception as e:
            logger.error(f'error uploading table: {e}')
            return False

    @staticmethod
    def upload(url: str, headers: list, config: str, data: str):
        r = requests.patch(url, headers=headers,
                           files={'config_file': config, 'data_file': data})
        logger.info(f'table upload status: {r.status_code}')
        return r

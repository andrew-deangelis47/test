import os
import requests
import csv

from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.datamigration import logger
from paperless.client import PaperlessClient
from decimal import Decimal
from datetime import date, datetime


class BaseM2MImportProcessor(BaseImportProcessor):

    @staticmethod
    def generate_normalized_value(value):
        if isinstance(value, Decimal):
            value = round(float(value), 4) if value is not None else 0
        elif isinstance(value, (date, datetime)):
            value = datetime.strftime(value, '%Y-%m-%d %H:%M:%S') if value is not None else 0
        else:
            if isinstance(value, str):
                value = value.strip()
            value = f'{value}' if value is not None else '0'
        return value


class BaseM2MImportResyncProcessor(BaseImportProcessor):

    def upload_retry(self, url: str, headers: list, config: str, data: str):
        try:
            r = self.upload(url, headers, config, data)
            if int(r.status_code) >= 500:
                r = self.upload(url, headers, config, data)
                if int(r.status_code) >= 500:
                    logger.error(f'Upload Failed: Something went wrong while retrying uploading the inventory table. '
                                 f'Please check the custom table`s integrity. http code {r.status_code} - {r.text}')
                    return False
        except Exception as e:
            logger.error(f'error uploading table: {e}')
            return False
        return True

    @staticmethod
    def upload(url: str, headers: list, config: str, data: str):
        r = requests.patch(url, headers=headers,
                           files={'config_file': config, 'data_file': data})
        logger.info(f'table upload status: {r.status_code}')
        logger.debug(f'table upload status: {r.text}')
        return r

    @staticmethod
    def file_clean_up(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)

    def recreate_table(self, config, headers, list_to_upload, table_name):
        config_file_path = '/tmp/resync_config.csv'
        self.file_clean_up(config_file_path)
        data_file_path = '/tmp/resync_data.csv'
        self.file_clean_up(data_file_path)

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
            for data_row in list_to_upload:
                logger.debug(data_row)
                data_writer.writerow(data_row)

        client = PaperlessClient.get_instance()
        headers = {'Authorization': 'API-Token {}'.format(client.access_token)}
        u_url = f'https://api.paperlessparts.com/suppliers/public/custom_tables/{table_name}'
        with open(data_file_path, 'rb') as data_stream:
            with open(config_file_path, 'rb') as config_stream:
                return self.upload_retry(u_url, headers, config_stream, data_stream)
        return False

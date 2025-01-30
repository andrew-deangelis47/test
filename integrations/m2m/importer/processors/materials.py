import csv

from typing import List
from paperless.client import PaperlessClient
from baseintegration.utils.custom_table import ImportCustomTable, HexImportCustomTable
from baseintegration.datamigration import logger
from m2m.models import Inmastx
from m2m.configuration import M2MConfiguration
from m2m.importer.processors.base import BaseM2MImportProcessor, BaseM2MImportResyncProcessor


class M2MMaterialBulkImportProcessor(BaseM2MImportProcessor):
    table_name = 'raw_materials'
    _m2m_config = M2MConfiguration()

    def _process(self, material_ids):
        return self.bulk_import(material_ids)

    def bulk_import(self, material_ids):
        self._m2m_config: M2MConfiguration = self._importer._m2m_config

        base_dict = self._importer.header_dict.copy()
        materials: List[dict] = []
        for material_id in material_ids:
            dict_to_upload = self.generate_table_data(material_id, base_dict)
            materials.append(dict_to_upload.copy())
            logger.info(f'adding {material_id} to bulk upload')
        result: dict = ImportCustomTable.upload_records(identifier=f'M2M-material-bulk-upload-count-{len(materials)}',
                                                        table_name=self.table_name,
                                                        records=materials)
        if len(result["failures"]) > 0:
            logger.info(f'imported {len(material_ids)} materials with {len(result["failures"])} failures')
            for failure in result["failures"]:
                errors = failure.get('error', [])
                for error in errors:
                    if "Custom table row uniqueness violation." in error.get('message', ''):
                        resync_processor = M2MResyncMaterialImporterProcessor(importer=self._importer)
                        hex_stamp = resync_processor.resync(hex_stamp='0x0000000000000000')
                        HexImportCustomTable.update_last_processed_hex_counter('import_material', hex_stamp)
                        return True
            return False
        logger.info(f'imported {len(material_ids)} materials without failures')
        return True

    def generate_table_data(self, material_id, headers: dict):
        row = Inmastx.objects.filter(fpartno=material_id).first()
        nr = self.slim_raw_material_row(row, headers)
        return nr

    def slim_raw_material_row(self, row: Inmastx, base_dict: dict):  # noqa: C901
        base_dict["fpartno"] = self.generate_normalized_value(row.fpartno)
        base_dict["frev"] = self.generate_normalized_value(row.frev)
        base_dict["fcudrev"] = self.generate_normalized_value(row.fcudrev)
        base_dict["fdescript"] = self.generate_normalized_value(row.fdescript)
        if self._m2m_config.material_use_total_cost:
            base_dict["f2totcost"] = self.generate_normalized_value(row.f2totcost)
        else:
            base_dict["fstdcost"] = self.generate_normalized_value(row.fstdcost)
        base_dict["fmeasure"] = self.generate_normalized_value(row.fmeasure)
        base_dict["frevdt"] = self.generate_normalized_value(row.frevdt)
        base_dict["identity_column"] = int(row.identity_column)
        if self._m2m_config.material_add_group_code:
            base_dict['fgroup'] = self.generate_normalized_value(row.fgroup)
        if self._m2m_config.material_add_product_class:
            base_dict['fprodcl'] = self.generate_normalized_value(row.fprodcl)
        return base_dict


class M2MMaterialImporterProcessor(M2MMaterialBulkImportProcessor):
    def _process(self, material_id):
        return self.bulk_import(material_ids=[material_id])


class M2MResyncMaterialImporterProcessor(M2MMaterialImporterProcessor, BaseM2MImportResyncProcessor):
    def _process(self, material_id):
        raise ValueError(f"_process() method not implemented on {self.__class__.__name__}")

    def resync(self, hex_stamp) -> str:
        self._m2m_config: M2MConfiguration = self._importer._m2m_config

        base_dict = self._importer.header_dict.copy()
        config, headers = ImportCustomTable.convert_dict(base_dict, self._importer._is_for_unique_key.copy())

        from django.db import connection
        cursor = connection.cursor()
        if self._m2m_config.material_use_total_cost:
            cost = 'f2totcost'
        else:
            cost = 'fstdcost'

        add_ons = ''
        if self._m2m_config.material_add_group_code:
            add_ons += 'fgroup,'
        if self._m2m_config.material_add_product_class:
            add_ons += 'fprodcl,'

        material_query = f"SELECT fpartno,frev, fcudrev,fdescript,{cost}, " \
                         f"fmeasure,frevdt,identity_column, {add_ons} timestamp_column " \
                         f"from M2MDATA20.dbo.inmastx " \
                         f"WHERE {self._m2m_config.material_condition} " \
                         f"ORDER BY timestamp_column ASC "
        cursor.execute(material_query)
        try:
            material_query_set = cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
        if len(material_query_set) < 1:
            logger.info('nothing to resync')
            return hex_stamp
        list_to_upload = self.generate_table_data(material_query_set, base_dict)

        config_file_path = '/tmp/bulk_material_config.csv'
        self.file_clean_up(config_file_path)
        data_file_path = '/tmp/bulk_material_data.csv'
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
                data_writer.writerow(data_row)

        client = PaperlessClient.get_instance()
        headers = {'Authorization': 'API-Token {}'.format(client.access_token)}
        url = f'https://api.paperlessparts.com/suppliers/public/custom_tables/{self.table_name}'
        with open(data_file_path, 'rb') as data_stream:
            with open(config_file_path, 'rb') as config_stream:
                self.upload_retry(url, headers, config_stream, data_stream)

        logger.info(f'resync import for material: {self.table_name}')
        hex_timestamp = f'0x{material_query_set[-1][-1].hex()}'
        logger.info(hex_timestamp)
        return hex_timestamp

    def generate_table_data(self, material_records, headers: dict):
        record_dict_list = []
        for row in material_records:
            record_dict_list.append(self.slim_raw_material_row(row, headers.copy()))
        return record_dict_list

    def slim_raw_material_row(self, row, base_dict: dict):  # noqa: C901
        base_dict["fpartno"] = self.generate_normalized_value(row[0])
        base_dict["frev"] = self.generate_normalized_value(row[1])
        base_dict["fcudrev"] = self.generate_normalized_value(row[2])
        base_dict["fdescript"] = self.generate_normalized_value(row[3])
        if self._m2m_config.material_use_total_cost:
            base_dict["f2totcost"] = self.generate_normalized_value(row[4])
        else:
            base_dict["fstdcost"] = self.generate_normalized_value(row[4])
        base_dict["fmeasure"] = self.generate_normalized_value(row[5])
        base_dict["frevdt"] = self.generate_normalized_value(row[6])
        n = 7
        base_dict["identity_column"] = int(row[n])

        if self._m2m_config.material_add_group_code:
            n += 1
            base_dict['fgroup'] = self.generate_normalized_value(row[n])
        if self._m2m_config.material_add_product_class:
            n += 1
            base_dict['fprodcl'] = self.generate_normalized_value(row[n])
        return base_dict


class M2MMaterialBulkPlaceholder:
    pass

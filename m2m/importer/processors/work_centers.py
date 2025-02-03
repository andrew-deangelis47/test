from baseintegration.utils.custom_table import ImportCustomTable
from m2m.models import Inwork, Inopds
from m2m.importer.processors.base import BaseM2MImportProcessor, BaseM2MImportResyncProcessor
from datamigration import logger
from typing import List, Tuple


class M2MWorkCenterBulkImportProcessor(BaseM2MImportProcessor):
    w_table_name = 'workcenters'
    op_table_name = 'op_descriptions'

    def _process(self, work_center_ids: List[str]) -> bool:
        return self.bulk_import(work_center_ids)

    def bulk_import(self, work_center_ids: List[str]) -> bool:

        w_data = []
        op_data = []
        for work_center_id in work_center_ids:
            wcc = work_center_id.strip()
            w_base_dict = self._importer.w_header_dict.copy()
            w_dict_to_upload = self.generate_w_table_data(wcc, w_base_dict)
            if w_dict_to_upload:
                w_data.append(w_dict_to_upload.copy())
            else:
                logger.warning(f'Could not find record for work-center code: {wcc}')

            op_base_dict = self._importer.op_header_dict.copy()
            op_dict_to_upload = self.generate_op_table_data(wcc, op_base_dict)
            op_data.extend(op_dict_to_upload.copy())
        w_results: dict = ImportCustomTable.upload_records(
            identifier=f'M2M-workcenter-id-bulk-upload-count-{len(w_data)}',
            records=w_data, table_name=self.w_table_name)
        op_results: dict = ImportCustomTable.upload_records(
            identifier=f'M2M-workcenter-op-description-bulk-upload-count-{len(op_data)}',
            records=op_data, table_name=self.op_table_name)
        if len(w_results["failures"]) > 0 or len(op_results["failures"]) > 0:
            logger.info(
                f'imported {len(work_center_ids)} workcenters with {len(w_results["failures"])} failures for codes')
            logger.info(
                f'imported {len(work_center_ids)} workcenters with {len(op_results["failures"])} failures for '
                f'op descriptions')
            result = False
            for failure in w_results["failures"]:
                errors = failure.get('error', [])
                for error in errors:
                    if "Custom table row uniqueness violation." in error.get('message', ''):
                        resync_processor = M2MResyncWorkCenterImporterProcessor(importer=self._importer)
                        resync_processor.resync()
                        result = True

            for failure in op_results["failures"]:
                errors = failure.get('error', [])
                for error in errors:
                    if "Custom table row uniqueness violation." in error.get('message', ''):
                        resync_processor = M2MResyncWorkCenterImporterProcessor(importer=self._importer)
                        resync_processor.resync()
                        result = True
            return result
        return True

    def generate_op_table_data(self, work_center_id, headers: dict) -> List[dict]:
        rows = Inopds.objects.filter(fcpro_id=work_center_id)
        nrs = []
        for row in rows:
            nr = self.slim_op_row(row, headers)
            nrs.append(nr.copy())
        return nrs

    def slim_op_row(self, row: Inopds, base_dict: dict) -> dict:  # noqa: C901
        base_dict["fdescnum"] = self.generate_normalized_value(row.fdescnum)
        base_dict["fcpro_id"] = self.generate_normalized_value(row.fcpro_id)
        base_dict["fnstd_prod"] = self.generate_normalized_value(row.fnstd_prod)
        base_dict["fnstd_set"] = self.generate_normalized_value(row.fnstd_set)
        base_dict["identity_column"] = int(row.identity_column)
        base_dict["fopmemo"] = self.generate_normalized_value(row.fopmemo)
        base_dict["fac"] = self.generate_normalized_value(row.fac)
        return base_dict

    def generate_w_table_data(self, work_center_id, headers: dict) -> dict:
        logger.info(f'getting {work_center_id}')
        row = Inwork.objects.filter(fcpro_id=work_center_id).first()
        nr = None
        if row:
            nr = self.slim_w_row(row, headers)
        return nr

    def slim_w_row(self, row: Inwork, base_dict: dict) -> dict:  # noqa: C901
        base_dict['fnavgwkhrs'] = self.generate_normalized_value(row.fnavgwkhrs)
        base_dict['fcpro_id'] = self.generate_normalized_value(row.fcpro_id)
        base_dict['fcpro_name'] = self.generate_normalized_value(row.fcpro_name)
        base_dict['fccomments'] = self.generate_normalized_value(row.fccomments)
        base_dict['fdept'] = self.generate_normalized_value(row.fdept)
        base_dict['flabcost'] = self.generate_normalized_value(row.flabcost)
        base_dict['fnavgque'] = self.generate_normalized_value(row.fnavgque)
        base_dict['flschedule'] = self.generate_normalized_value(row.flschedule)
        base_dict['fnmax1'] = self.generate_normalized_value(row.fnmax1)
        base_dict['fnmax2'] = self.generate_normalized_value(row.fnmax2)
        base_dict['fnmax3'] = self.generate_normalized_value(row.fnmax3)
        base_dict['fnmaxque'] = self.generate_normalized_value(row.fnmaxque)
        base_dict['fnpctutil'] = self.generate_normalized_value(row.fnpctutil)
        base_dict['fnqueallow'] = self.generate_normalized_value(row.fnqueallow)
        base_dict['fnstd1'] = self.generate_normalized_value(row.fnstd1)
        base_dict['fnstd2'] = self.generate_normalized_value(row.fnstd2)
        base_dict['fnstd3'] = self.generate_normalized_value(row.fnstd3)
        base_dict['fnstd_prod'] = self.generate_normalized_value(row.fnstd_prod)
        base_dict['fnstd_set'] = self.generate_normalized_value(row.fnstd_set)
        base_dict['fnsumdur'] = self.generate_normalized_value(row.fnsumdur)
        base_dict['fovrhdcost'] = self.generate_normalized_value(row.fovrhdcost)
        base_dict['fscheduled'] = self.generate_normalized_value(row.fscheduled)
        base_dict['fspandays'] = self.generate_normalized_value(row.fspandays)
        base_dict['fnpque'] = self.generate_normalized_value(row.fnpque)
        base_dict['flconstrnt'] = self.generate_normalized_value(row.flconstrnt)
        base_dict['identity_column'] = self.generate_normalized_value(row.identity_column)
        base_dict['fac'] = self.generate_normalized_value(row.fac)
        base_dict['fcstdormax'] = self.generate_normalized_value(row.fcstdormax)
        base_dict['fndbrmod'] = self.generate_normalized_value(row.fndbrmod)
        base_dict['fnloadcapc'] = self.generate_normalized_value(row.fnloadcapc)
        base_dict['fnmaxcapload'] = self.generate_normalized_value(row.fnmaxcapload)
        base_dict['flaltset'] = self.generate_normalized_value(row.flaltset)
        base_dict['fcsyncmisc'] = self.generate_normalized_value(row.fcsyncmisc)
        base_dict['queuehrs'] = self.generate_normalized_value(row.queuehrs)
        base_dict['constbuff'] = self.generate_normalized_value(row.constbuff)
        base_dict['resgroup'] = self.generate_normalized_value(row.resgroup)
        base_dict['flbflabor'] = self.generate_normalized_value(row.flbflabor)
        base_dict['cycleunits'] = self.generate_normalized_value(row.cycleunits)
        base_dict['simopstype'] = self.generate_normalized_value(row.simopstype)
        base_dict['size'] = self.generate_normalized_value(row.size)
        base_dict['canbreak'] = self.generate_normalized_value(row.canbreak)
        base_dict['sizeum'] = self.generate_normalized_value(row.sizeum)
        base_dict['timefence'] = self.generate_normalized_value(row.timefence)
        base_dict['fcgroup'] = self.generate_normalized_value(row.fcgroup)
        base_dict['fracsimops'] = self.generate_normalized_value(row.fracsimops)
        return base_dict


class M2MWorkCenterImportProcessor(M2MWorkCenterBulkImportProcessor):

    def _process(self, work_center_id: str):
        return self.bulk_import([work_center_id])


class M2MResyncWorkCenterImporterProcessor(M2MWorkCenterImportProcessor, BaseM2MImportResyncProcessor):
    def _process(self, material_id):
        raise ValueError(f"_process() method not implemented on {self.__class__.__name__}")

    def resync(self) -> bool:

        from django.db import connection
        cursor = connection.cursor()

        work_center_code_query = "SELECT fcpro_id FROM Inwork "
        cursor.execute(work_center_code_query)
        try:
            work_center_codes_set = cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

        w_base_dict = self._importer.w_header_dict.copy()
        w_config, w_headers = ImportCustomTable.convert_dict(w_base_dict, ['fcpro_id'])

        op_base_dict = self._importer.op_header_dict.copy()
        op_config, op_headers = ImportCustomTable.convert_dict(op_base_dict, ['fcpro_id', 'fdescnum'])

        w_list_to_upload, op_list_to_upload = \
            self.generate_table_data(work_center_codes_set, {'w': w_base_dict, 'op': op_base_dict})

        w_result = self.recreate_table(config=w_config,
                                       headers=w_headers,
                                       list_to_upload=w_list_to_upload,
                                       table_name=self.w_table_name)

        op_result = self.recreate_table(config=op_config,
                                        headers=op_headers,
                                        list_to_upload=op_list_to_upload,
                                        table_name=self.op_table_name)

        logger.info('resync import for workcenter tables complete')
        return w_result and op_result

    def generate_table_data(self, work_center_codes_set: List[Tuple], headers: dict):
        w_list_to_upload = []
        op_list_to_upload = []
        for work_center_code in work_center_codes_set:
            wcc = f"{work_center_code[0]}".strip()
            w_dict_to_upload = self.generate_w_table_data(wcc, headers['w'].copy())
            if w_dict_to_upload:
                w_list_to_upload.append(w_dict_to_upload.copy())
            op_dict_to_upload = self.generate_op_table_data(wcc, headers['op'].copy())
            op_list_to_upload.extend(op_dict_to_upload.copy())
        return w_list_to_upload, op_list_to_upload


class M2MWorkCenterBulkPlaceholder:
    pass

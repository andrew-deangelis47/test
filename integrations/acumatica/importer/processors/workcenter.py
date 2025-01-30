from paperless.client import PaperlessClient

from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import custom_table_patch

from acumatica.api_models.acumatica_models import WorkCenter
from acumatica.api_models.paperless_custom_tables import WorkCenterCustomTableFormat


class AcumaticaWorkCenterImportProcessor(BaseImportProcessor):

    @staticmethod
    def format_as_row(work_center: WorkCenter, overhead_rate: float):
        data = dict(work_center=work_center.get('WorkCenterID', dict()).get("value"),
                    description=work_center.get('Description', dict()).get('value'),
                    standard_cost=work_center.get('StandardCost', dict()).get('value'),
                    overhead=overhead_rate,
                    location=work_center.get('Location', dict()).get('value') if work_center.get('Location', dict()).get('value') != '{}' else '',  # TODO attrs not converting empty dict to string by default
                    is_outside_service=work_center.get('OutsideProcessing', dict()).get('value'))
        return data

    @staticmethod
    def format_value(value, model):
        if isinstance(value, model):
            return value
        else:
            return model

    def _process(self, work_center_id: str) -> bool:
        logger.info(f'Processing work center {work_center_id}')
        params = {"$expand": "Overheads"}
        work_center: WorkCenter = WorkCenter.get_by_id(id=work_center_id, params=params, skip_serializer=True)
        table_model = WorkCenterCustomTableFormat
        work_center_row = self.format_as_row(work_center=work_center, overhead_rate=0)
        # TODO parent class should probably just do this
        id_name: str = table_model._primary_key
        table_name: str = table_model._custom_table_name
        url = f"suppliers/public/custom_tables/{table_name}/row"
        paperless_client: PaperlessClient = PaperlessClient.get_instance()
        custom_table_patch(client=paperless_client, data=dict(row_data=work_center_row), url=url, identifier=id_name)
        return True

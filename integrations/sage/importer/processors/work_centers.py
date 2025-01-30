from paperless.client import PaperlessClient
from typing import List
from baseintegration.datamigration import logger
from baseintegration.importer.import_processor import BaseImportProcessor
from baseintegration.utils import custom_table_patch
from sage.sage_api.client import SageImportClient
from sage.models.paperless_custom_tables.work_centers import WorkCenter as PaperlessWorkCenter
from sage.models.paperless_custom_tables.standard_operation import StandardOperation as StandardOperationCustTable
from sage.models.sage_models.work_center.work_center_full_entity import WorkCenterFullEntity
from sage.sage_api.filter_generation.work_center_filter_generator import WorkCenterFilterGenerator
from sage.models.sage_models.standard_operations import StandardOperation, StandardOperationFullEntity


class SageBulkWorkCenterImportProcessor(BaseImportProcessor):

    @staticmethod
    def map_work_center_type(work_center_type: int) -> str:
        WORK_CENTER_TYPE_MAPPING = [
            'Machine',
            'Labor',
            'Subcontracting'
        ]

        return WORK_CENTER_TYPE_MAPPING[work_center_type - 1]

    @staticmethod
    def format_work_center_as_row(work_center: WorkCenterFullEntity, work_center_type_string: str):
        data = {
            'work_center_id': work_center.work_center.work_center_id,
            'full_description': work_center.extra_info.description,
            'site': work_center.work_center.site,
            'cost_dimension': work_center.work_center.cost_dimension,
            'work_center_type': work_center_type_string,
        }
        return data

    @staticmethod
    def format_standard_op_as_row(standard_op: StandardOperation):
        data = {
            'standard_operation': standard_op.standard_operation,
            'description': standard_op.description,
            'main_work_center': standard_op.main_work_center,
            'rate': standard_op.rate
        }
        return data

    def _process(self, raw_work_center_ids: List[str]) -> bool:
        paperless_client: PaperlessClient = PaperlessClient.get_instance()
        sage_client = SageImportClient.get_instance()

        for work_center_id in raw_work_center_ids:
            self._process_work_center(work_center_id, paperless_client, sage_client)
            self._process_work_center_standard_operations(work_center_id, paperless_client, sage_client)

        return True

    def _process_work_center(self, work_center_id: str, paperless_client: PaperlessClient, sage_client: SageImportClient) -> bool:
        # 1) get the work center from the sage api and convert to custom table row
        work_center = sage_client.get_resource(
            WorkCenterFullEntity,
            WorkCenterFilterGenerator.get_filter_by_id(work_center_id),
            False
        )
        work_center_type_string = self.map_work_center_type(int(work_center.work_center.work_center_type))
        raw_work_center_row = self.format_work_center_as_row(work_center=work_center, work_center_type_string=work_center_type_string)

        # 2) Setup custom table information
        table_model = PaperlessWorkCenter
        table_model.work_center_id = raw_work_center_row['work_center_id']
        table_model.full_description = raw_work_center_row['full_description']
        table_model.site = raw_work_center_row['site']
        table_model.cost_dimension = raw_work_center_row['cost_dimension']
        table_model.work_center_type = raw_work_center_row['work_center_type']
        table_name: str = table_model._custom_table_name

        # 3) Make the call to update the custom table with the raw material
        url = f"suppliers/public/custom_tables/{table_name}/row"
        custom_table_patch(client=paperless_client, data=dict(row_data=raw_work_center_row), url=url,
                           identifier=f'Work Center: {work_center_id}')

    def _process_work_center_standard_operations(self, work_center_id: str, paperless_client: PaperlessClient, sage_client: SageImportClient) -> bool:
        # 1) get all standard ops for the work center
        standard_ops = sage_client.get_resource(
            StandardOperationFullEntity,
            WorkCenterFilterGenerator.get_filter_by_id(work_center_id)
        )

        for standard_op in standard_ops:

            raw_standard_op_row = self.format_standard_op_as_row(standard_op=standard_op.standard_operation)

            # 2) Setup custom table information
            table_model = StandardOperationCustTable
            table_model.standard_operation = raw_standard_op_row['standard_operation']
            table_model.main_work_center = raw_standard_op_row['main_work_center']
            table_model.rate = raw_standard_op_row['rate']
            table_name: str = table_model._custom_table_name

            # 3) Make the call to update the custom table with the standard operation
            url = f"suppliers/public/custom_tables/{table_name}/row"
            custom_table_patch(client=paperless_client, data=dict(row_data=raw_standard_op_row), url=url,
                               identifier=f'Standard Operation for {work_center_id}: {raw_standard_op_row["standard_operation"]}')

        logger.info('\n')


class SageWorkCenterImportProcessor(SageBulkWorkCenterImportProcessor):
    def _process(self, component_id: str) -> bool:
        logger.info(f"the component {component_id}")
        return super()._process([component_id])


class SageWorkCenterBulkPlaceholder:
    pass

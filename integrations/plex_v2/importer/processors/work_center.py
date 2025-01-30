from typing import List
from baseintegration.utils import custom_table_patch
from paperless.client import PaperlessClient
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex_v2.objects.work_center_import import WorkCenterImportDataSource
from baseintegration.datamigration import logger
from plex_v2.importer.processors.base import PlexImportProcessor


class WorkCenterBulkImportProcessor(PlexImportProcessor):

    def _process(self, work_center_codes: List[str]):
        client = PaperlessClient.get_instance()
        url = f"suppliers/public/custom_tables/{self._importer._paperless_table_model._custom_table_name}/row"

        for work_center_code in work_center_codes:
            logger.info(f"Processing work center {work_center_code}")

            # 1) get work center info
            work_center: WorkCenterImportDataSource = WorkCenterImportDataSource.get(work_center_code)

            # 2) convert to custom table row and update
            row = self._importer.work_center_custom_table_row_factory.to_custom_table_row(work_center)

            try:
                custom_table_patch(client=client, data=dict(row_data=row), url=url, identifier=f'Work Center {work_center.Name}')
            except Exception as e:
                raise CancelledIntegrationActionException(e)

        return True


class WorkCenterImportProcessor(WorkCenterBulkImportProcessor):
    def _process(self, work_center: WorkCenterImportDataSource) -> bool:
        return super()._process([work_center])


class WorkCenterBulkPlaceholder:
    pass

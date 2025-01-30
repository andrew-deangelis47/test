from plex_v2.objects.work_center_import import WorkCenterImportDataSource
from typing import List


class PLEXWorkCenterListener:
    identifier = "work_center_import"

    def __init__(self, integration, erp_config):
        self._integration = integration
        self._erp_config = erp_config

    def get_new(self, bulk=False):
        """
        Heads up - we cannot sense updates to work centers with this data source - should only be run weekly
        Instead of return a list of codes we will return a list of work center models to limit the processing, otherwise we'd be making
        a call to list all the workcenters for each workcenter (AKA number of workcenters^2 would be requested on each run)
        """

        work_center_codes = []
        work_centers: List[WorkCenterImportDataSource] = WorkCenterImportDataSource.get_all()
        work_center: WorkCenterImportDataSource
        for work_center in work_centers:
            work_center_codes.append(work_center.Workcenter_Code)

        return work_center_codes

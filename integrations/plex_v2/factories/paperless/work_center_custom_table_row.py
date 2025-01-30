from plex_v2.configuration import PlexConfig
from plex_v2.objects.work_center_import import WorkCenterImportDataSource
from pytz import timezone
from pendulum.datetime import DateTime


class WorkCenterCustomTableRowFactory:

    def __init__(self, erp_config: PlexConfig):
        self.erp_config = erp_config

    def to_custom_table_row(self, work_center: WorkCenterImportDataSource):
        return {
            "Workcenter_Code": work_center.Workcenter_Code,
            "Name": work_center.Name,
            "Direct_Labor_Cost": work_center.Direct_Labor_Cost,
            "Other_Burden_Cost": work_center.Other_Burden_Cost,
            "Last_Import_Time": self._get_current_time()
        }

    def _get_current_time(self) -> str:
        tz = timezone('EST5EDT')
        return (str(DateTime.now(tz))[0:19]).replace('T', ' ')

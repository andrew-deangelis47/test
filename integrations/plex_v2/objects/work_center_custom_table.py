from pydantic import Field

from plex_v2.objects.custom_table import CustomTableFormat


class WorkCenterCustomTable(CustomTableFormat):
    _custom_table_name = "work_center_integration_import"  # This is what will appear in paperless, and how the table will be referenced
    _primary_key = "Workcenter_Code"

    def __init__(self):
        self.Workcenter_Code: str = Field(alias="Workcenter_Code")
        self.Name: str = Field(alias="Name")
        self.Direct_Labor_Cost: str = Field(alias="Direct_Labor_Cost")
        self.Other_Burden_Cost = Field(alias="Other_Burden_Cost")
        self.Last_Import_Time = Field(alias="Last_Import_Time")

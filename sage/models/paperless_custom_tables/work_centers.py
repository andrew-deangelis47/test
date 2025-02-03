from pydantic import Field
from sage.models.paperless_custom_tables.custom_table import CustomTableFormat


class WorkCenter(CustomTableFormat):
    _custom_table_name = "work_centers"  # This is what will appear in paperless, and how the table will be referenced
    _primary_key = "work_center_id"

    def __init__(self):
        self.work_center_id: str = Field(alias="Work_center_id")
        self.site: str = Field(alias="manufacturing_site")
        self.cost_dimension = Field(alias="manufacturing_site")
        self.work_center_type = Field(alias="manufacturing_site")
        self.full_description = Field(alias="full_description")

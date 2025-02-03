from pydantic import Field
from sage.models.paperless_custom_tables.custom_table import CustomTableFormat


class StandardOperation(CustomTableFormat):
    _custom_table_name = "standard_operations"  # This is what will appear in paperless, and how the table will be referenced
    _primary_key = "standard_operation"

    def __init__(self):
        self.standard_operation: str = Field(alias="standard_operation")
        self.description: str = Field(alias="description")
        self.main_work_center: str = Field(alias="main_work_center")
        self.rate: str = Field(alias="rate")

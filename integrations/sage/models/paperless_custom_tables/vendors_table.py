from pydantic import Field
from sage.models.paperless_custom_tables.custom_table import CustomTableFormat


class VendorsTable(CustomTableFormat):
    _custom_table_name = "vendors_custom_table"
    _primary_key = "vendor_id"  # This

    def __init__(self):
        self.vendor_id: str = Field(alias="vendor_id")
        self.name: str = Field(alias="name")

from pydantic import Field

from plex_v2.objects.custom_table import CustomTableFormat


class VendorCustomTable(CustomTableFormat):
    _custom_table_name = "vendor_integration_import"  # This is what will appear in paperless, and how the table will be referenced
    _primary_key = "Supplier_Code"

    def __init__(self):
        self.Supplier_Code: str = Field(alias="Supplier_Code")
        self.Supplier_Name: str = Field(alias="Supplier_Name")
        self.Category: str = Field(alias="Category")
        self.Type: str = Field(alias="Type")
        self.Status: str = Field(alias="Status")
        self.Last_Import_Time = Field(alias="Last_Import_Time")

from plex_v2.objects.custom_table import CustomTableFormat
from pydantic import Field


class TestCustomTableFormat:

    def test_create_table_header(self):

        class CustomTableWrapper(CustomTableFormat):
            def __init__(self):
                self.Supplier_Code: str = Field(alias="Supplier_Code")
                self.Supplier_Name: str = Field(alias="Supplier_Name")
                self.Category: str = Field(alias="Category")
                self.Type: str = Field(alias="Type")
                self.Status: str = Field(alias="Status")
                self.Last_Import_Time = Field(alias="Last_Import_Time")

        ct = CustomTableWrapper()
        header = ct.create_paperless_table_header_sample()
        assert 'Supplier_Code' in header.keys()
        assert 'Supplier_Name' in header.keys()
        assert 'Category' in header.keys()
        assert 'Type' in header.keys()
        assert 'Status' in header.keys()
        assert 'Last_Import_Time' in header.keys()

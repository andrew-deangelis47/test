from plex_v2.objects.vendor_custom_table import VendorCustomTable


class TestVendorCustomTable:

    def test_create_table_header(self):

        vct = VendorCustomTable()

        header = vct.create_paperless_table_header_sample()
        assert 'Supplier_Code' in header.keys()
        assert 'Supplier_Name' in header.keys()
        assert 'Category' in header.keys()
        assert 'Type' in header.keys()
        assert 'Status' in header.keys()
        assert 'Last_Import_Time' in header.keys()

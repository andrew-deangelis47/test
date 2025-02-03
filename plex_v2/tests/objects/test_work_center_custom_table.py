from plex_v2.objects.work_center_custom_table import WorkCenterCustomTable


class TestWorkCenterCustomTable:

    def test_create_table_header(self):

        wcct = WorkCenterCustomTable()

        header = wcct.create_paperless_table_header_sample()
        assert 'Workcenter_Code' in header.keys()
        assert 'Name' in header.keys()
        assert 'Direct_Labor_Cost' in header.keys()
        assert 'Other_Burden_Cost' in header.keys()
        assert 'Last_Import_Time' in header.keys()

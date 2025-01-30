import json
from unittest.mock import patch
from plex_v2.client import PlexClient
import os
from plex_v2.objects.bom_upload_datasource import BomUploadDatasource


class TestBomUploadDatasource:
    def setup_method(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), "../data/bom_ds_out.json"), 'r') as f:
            self.mock_part = json.load(f)
            PlexClient()  # Initialize the singleton
            self.maxDiff = 650

    def test_create(self):
        with patch.object(PlexClient, 'create_resource', return_value=self.mock_part):
            bom_upload_ds = BomUploadDatasource(
                Component_Part_No='Component_Part_No',
                Operation_Code='Operation_Code',
                Part_No='Part_No',
                Quantity=1,
                Auto_Deplete=1,
                Component_Revision='Component_Revision',
                Component_Type='Component_Type',
                Engineering_Quantity=1.43,
                Fixed_Loss=3.23,
                Fixed_Qty=5,
                Max_Qty=9.4,
                Min_Qty=1.2,
                Note='Note',
                Operation_No=10,
                Position='Position',
                Revision='Revision',
                Scaling=3,
                Sort_Order=4.3,
                Transfer_Heat=3,
                Unit_Conversion='Unit_Conversion',
                Validate=0,
                Yield_Management_Enabled=True,
                Yield_Percentage=3.4
            )

            bom_upload_ds.create()

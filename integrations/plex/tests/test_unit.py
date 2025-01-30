# import standard libraries
import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))
from plex.objects.unit import Unit
from baseintegration.integration import Integration

import requests_mock


@pytest.fixture
def setup_export_order():
    integration = Integration()
    from plex.exporter.exporter import PlexOrderExporter
    i = PlexOrderExporter(integration)
    return i


class TestUnit:
    def test_unit_find(self, setup_export_order):
        with requests_mock.Mocker(real_http=True) as mock:
            jsona = '[{"id": "b09015e9-9fc3-4692-b831-20f3aeed2ebf","unit": "test","denominatorUnit": "string","ediCode": "string","weightUnit": false,"pieceUnit": false,"hourUnit": false,"dayUnit": false,"weekUnit": false,"monthUnit": false,"yearUnit": false,"unitStandard": "string","areaUnit": false,"reference": "string"}]'
            mock.get("https://test.connect.plex.com/edi/v1/units",
                     text=jsona,
                     status_code=200)
            units = Unit.find_units(unit_name='test')
            assert len(units) == 1
            assert units[0].id == "b09015e9-9fc3-4692-b831-20f3aeed2ebf"

# import standard libraries
import pytest
import os

# append to path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))
from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_order


@pytest.fixture
def setup_integration():
    integration = Integration()
    """Create integration and register the customer processor to process orders"""
    from e2_cloud.exporter.exporter import E2CloudOrderExporter
    i = E2CloudOrderExporter(integration)
    return i


class TestE2Cloud:
    """Runs tests against a dummy database using models.py"""

    def test_non_assembly(self, setup_integration):
        item_list = setup_integration._process_order(get_order(1))
        assert len(item_list) == 4
        assert str(item_list[0][0]) == "043021"
        assert str(item_list[0][1]) == "1"
        assert str(item_list[0][2]) == "Test Part.PDF"
        assert str(item_list[3][0]) == "042821"

    def test_assembly_mix(self, setup_integration):
        item_list = setup_integration._process_order(get_order(33))
        assert len(item_list) == 7
        assert str(item_list[0][0]) == "BOM Level"
        assert str(item_list[1][0]) == "1"
        assert str(item_list[2][0]) == "2"
        assert str(item_list[3][0]) == "2.1"
        assert str(item_list[4][0]) == "2.2"
        assert str(item_list[5][0]) == "2.3"
        assert str(item_list[6][0]) == "2.3.1"
        assert str(item_list[1][1]) == "PARTYPART"
        assert str(item_list[6][1]) == "1054part"

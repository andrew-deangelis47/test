# import standard libraries
import pytest
import os

# append to path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))
from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_quote
from hubspot.utils import HubspotQuote


@pytest.fixture
def setup_integration():
    integration = Integration()
    """Create integration and register the customer processor to process orders"""
    from hubspot.exporter.exporter import HubspotQuoteExporter
    i = HubspotQuoteExporter(integration)
    return i


class TestHubspot:

    def test_process_single_quote(self, setup_integration, caplog):
        setup_integration._setup_erp_config()
        setup_integration._register_default_processors()
        setup_integration._process_quote(get_quote(6))
        assert "Processing quote 6" in caplog.text
        assert "Quote 6 was processed" in caplog.text

    def test_utils_init(self, setup_integration):
        setup_integration._setup_erp_config()
        setup_integration._register_default_processors()
        hubspot_quote = HubspotQuote()
        assert hubspot_quote.name == "n/a"

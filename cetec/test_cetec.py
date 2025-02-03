# import standard libraries
import pytest
import os
import requests_mock

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
    from cetec.exporter.exporter import CetecOrderExporter
    i = CetecOrderExporter(integration)
    return i


class TestCetec:
    """Runs tests against a dummy database using models.py"""

    def test_process_order(self, setup_integration, caplog):
        with requests_mock.Mocker(real_http=True) as mock:
            mock.post("https://testapi.com/api/partrevisiondefinition", status_code=200, text="")
            mock.post("https://testapi.com/importjson/quotes", status_code=200,
                      text='{"quotes":[8348],"orders":[],"message":"","success":1}')
            setup_integration._process_order(get_order(53))

            log = caplog.text
            assert "customer_name is: Maine Blueberry Co" in log
            assert "customer_id is: MAINE" in log

            assert "Processing order 53" in log
            assert "Request URL: " in log
            assert "Request JSON payload:" in log
            assert "Response status code: " in log
            assert "Response content: " in log

    # tests process_order on an order with internal notes
    def test_internal_notes(self, setup_integration, caplog):
        with requests_mock.Mocker(real_http=True) as mock:
            mock.post("https://testapi.com/api/partrevisiondefinition", status_code=200, text="")
            mock.post("https://testapi.com/importjson/quotes", status_code=200,
                      text='{"quotes":[8348],"orders":[],"message":"","success":1}')
            setup_integration._process_order(get_order(28))

            log = caplog.text
            assert "customer_name is: Maine Blueberry Co" in log
            assert "customer_id is: MAINE" in log

            assert "Order Number:" in log
            assert "Request URL: " in log
            assert "Request JSON payload:" in log
            assert "Response status code: " in log
            assert "Response content: " in log

    def test_purchase_order(self, setup_integration, caplog):
        with requests_mock.Mocker(real_http=True) as mock:
            mock.post("https://testapi.com/api/partrevisiondefinition", status_code=200, text="")
            mock.post("https://testapi.com/importjson/quotes", status_code=200,
                      text='{"quotes":[8348],"orders":[],"message":"","success":1}')
            setup_integration._process_order(get_order(32))

            log = caplog.text
            assert "customer_name is: Maine Blueberry Co" in log
            assert "customer_id is: MAINE" in log

            assert "Setting purchase order" in log
            assert "Request URL: " in log
            assert "Request JSON payload:" in log
            assert "Response status code: " in log
            assert "Response content: " in log

    def test_purchase_order_with_pickup(self, setup_integration, caplog):
        with requests_mock.Mocker(real_http=True) as mock:
            mock.post("https://testapi.com/api/partrevisiondefinition", status_code=200, text="")
            mock.post("https://testapi.com/importjson/quotes", status_code=200,
                      text='{"quotes":[8348],"orders":[],"message":"","success":1}')
            setup_integration._process_order(get_order(4))

            log = caplog.text
            assert "customer_name is: Maine Blueberry Co" in log
            assert "customer_id is: MAINE" in log

            assert "Ship via is pickup" in log
            assert "Request URL: " in log
            assert "Request JSON payload:" in log
            assert "Response status code: " in log
            assert "Response content: " in log

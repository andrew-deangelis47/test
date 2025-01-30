# import standard libraries
import pytest
import os
import requests_mock

# append to path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))
from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_quote


@pytest.fixture
def setup_integration():
    integration = Integration()
    """Create integration and register the customer processor to process orders"""
    from lillyworks.exporter.exporter import LillyWorksQuoteExporter
    i = LillyWorksQuoteExporter(integration)
    return i


class TestLillyworks:
    """Runs tests against a dummy database using models.py"""

    def test_process_single_quote_create_customer(self, setup_integration, caplog):
        with requests_mock.Mocker(real_http=True) as mock:
            mock.post("https://app.lillyworks.net/account/logindirect", text="", status_code=200,
                      headers={"x-bearer-token": "blah", "x-application-url": "https://gc.app.lillyworks.net/00000_000/"})
            mock.post("https://gc.app.lillyworks.net/00000_000/api/data/postupsert", text="", status_code=200)
            mock.get("https://gc.app.lillyworks.net/00000_000/api/data/customers", text="[]", status_code=200)
            mock.get("https://gc.app.lillyworks.net/00000_000/api/data/TermsDefinitions",
                     text='[{"TermsDefinitionID": "30"}]', status_code=200)
            setup_integration._process_quote(get_quote(6))
            log = caplog.text
            assert "Testing quote connection" in log
            assert "Did not find a customer. Adding it to DB" in log
            assert "Adding quote item" in log
            assert "Adding pricing information" in log
            assert "Completed!" in log

    def test_process_single_quote_found_customer(self, setup_integration, caplog):
        with requests_mock.Mocker(real_http=True) as mock:
            mock.post("https://app.lillyworks.net/account/logindirect", text="", status_code=200,
                      headers={"x-bearer-token": "blah", "x-application-url": "https://gc.app.lillyworks.net/00000_000/"})
            mock.post("https://gc.app.lillyworks.net/00000_000/api/data/postupsert", text="", status_code=200)
            mock.get("https://gc.app.lillyworks.net/00000_000/api/data/customers", text='[{"CustomerID": "1234"}]', status_code=200)
            mock.get("https://gc.app.lillyworks.net/00000_000/api/data/TermsDefinitions",
                     text='[{"TermsDefinitionID": "30"}]', status_code=200)
            setup_integration._process_quote(get_quote(6))
            log = caplog.text
            assert "Testing quote connection" in log
            assert "Found one customer match" in log
            assert "Getting the terms definition for net 30" in log
            assert "Completed!" in log

    def test_process_single_quote_found_terms_def(self, setup_integration, caplog):
        with requests_mock.Mocker(real_http=True) as mock:
            mock.post("https://app.lillyworks.net/account/logindirect", text="", status_code=200,
                      headers={"x-bearer-token": "blah", "x-application-url": "https://gc.app.lillyworks.net/00000_000/"})
            mock.post("https://gc.app.lillyworks.net/00000_000/api/data/postupsert", text="", status_code=200)
            mock.get("https://gc.app.lillyworks.net/00000_000/api/data/customers",
                     text='[{"CustomerID": "1234", "TermsDefinitionID": "123"}]', status_code=200)
            setup_integration._process_quote(get_quote(6))
            log = caplog.text
            assert "Testing quote connection" in log
            assert "Found one customer match" in log
            assert "Terms definition found on customer. Using it" in log
            assert "Completed!" in log

    def test_process_single_quote_line_items(self, setup_integration, caplog):
        with requests_mock.Mocker(real_http=True) as mock:
            mock.post("https://app.lillyworks.net/account/logindirect", text="", status_code=200,
                      headers={"x-bearer-token": "blah", "x-application-url": "https://gc.app.lillyworks.net/00000_000/"})
            mock.post("https://gc.app.lillyworks.net/00000_000/api/data/postupsert", text="", status_code=200)
            mock.get("https://gc.app.lillyworks.net/00000_000/api/data/customers",
                     text='[{"CustomerID": "1234", "TermsDefinitionID": "123"}]', status_code=200)
            setup_integration._process_quote(get_quote(6))
            log = caplog.text
            assert "At LineNo 1" in log
            assert "At LineNo 2" in log
            assert "At LineNo 3" in log
            assert "At LineNo 4" in log
            assert "Completed!" in log

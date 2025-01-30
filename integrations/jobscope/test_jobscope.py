# import standard libraries
import os
import pytest

# append to path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))
from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_order
import requests_mock
import json
from jobscope.data.responses import CUSTOMER_RESPONSE, CONTACT_RESPONSE, PART_RESPONSE, SITE_RESPONSE
from paperless.objects.purchased_components import PurchasedComponent
from paperless.objects.customers import Account


class TestJobscope:
    """Runs tests against a dummy database using models.py"""

    def test_jobscope(self, caplog):
        integration = Integration()
        """Create integration and register the customer processor to process orders"""
        from jobscope.exporter.exporter import JobscopeOrderExporter
        with requests_mock.Mocker(real_http=True) as mock:
            """Create integration and register the customer processor to process orders"""
            mock.post("http://testapi.com/token/user", text='{"access_token": "blah"}', status_code=200)
            mock.post("http://testapi.com/api/RoutingHeaders", text="{}", status_code=200)
            mock.post("http://testapi.com/api/PartRoutings", text="{}", status_code=200)
            mock.post("http://testapi.com/api/Jobs", text='{"jobNumber": "123"}', status_code=200)
            mock.put("http://testapi.com/api/Jobs?JobNumber=123", text='{"jobNumber": "123"}', status_code=200)
            mock.put("http://testapi.com/api/Releases?ReleaseNumber=123", text="{}", status_code=200)
            mock.post("http://testapi.com/api/ReleaseLineItems", text="{}", status_code=200)
            mock.post("http://testapi.com/api/BillOfMaterialComponents", text="{}", status_code=200)
            customer_text = json.dumps(CUSTOMER_RESPONSE).replace("replace_me", "MAINE").replace("insert_code",
                                                                                                 "123")
            mock.get("http://testapi.com/api/Customers?CustomerNumber=MAINE", text=customer_text,
                     status_code=200)
            mock.post("http://testapi.com/api/Parts", text="{}", status_code=200)
            mock.get("http://testapi.com/api/Parts?PartNumber", text='{}', status_code=200)
            part_text = json.dumps(PART_RESPONSE).replace("replace_me", "042821")
            mock.get("http://testapi.com/api/Parts?PartNumber=042821", text=part_text, status_code=200)

            i = JobscopeOrderExporter(integration)
            i._process_order(get_order(3))
            assert "Part 043021 not found, need to create a new part" in caplog.text
            assert "Part 040821 not found, need to create a new part" in caplog.text
            assert "Part 042921 not found, need to create a new part" in caplog.text
            assert "Part 042821 was found, not creating a new part" in caplog.text
            assert "Processing operations for 043021" in caplog.text
            assert "Processing operations for 042821" not in caplog.text
            assert "Not creating BOM for item 043021 as it is either old, hardware, or does not have any children" in caplog.text
            assert "Creating job for order 3" in caplog.text
            assert "Creating line item 4 for order 3" in caplog.text

            # test assembly
            i._process_order(get_order(8))
            assert "Creating BOM for item 315" in caplog.text

    def test_account_importer(self, caplog):
        import random
        acct_code = str(random.randint(1, 100000000000))
        acct_name = f"account{acct_code}"
        with requests_mock.Mocker(real_http=True) as mock:
            mock.post("http://testapi.com/token/user", text='{"access_token": "blah"}', status_code=200)
            customer_text = json.dumps(CUSTOMER_RESPONSE).replace("replace_me", acct_name).replace("insert_code",
                                                                                                   acct_code)
            mock.get(f"http://testapi.com/api/Customers?CustomerNumber={acct_code}", text=customer_text,
                     status_code=200)
            contact_text = json.dumps(CONTACT_RESPONSE).replace("replace_me", acct_name).replace("insert_code",
                                                                                                 acct_code)
            mock.get("http://testapi.com/api/CustomerContacts?IncludeinActive=false&CustomerId=123", text=contact_text,
                     status_code=200)
            site_text = json.dumps(SITE_RESPONSE)
            mock.get("http://testapi.com/api/CustomerSites?IncludeinActive=false&CustomerId=123", text=site_text,
                     status_code=200)
            integration = Integration()
            """Create integration and register the customer processor to process orders"""
            from jobscope.importer.importer import JobscopeAccountImporter
            i = JobscopeAccountImporter(integration)
            i.run(acct_code)
            assert f"Account id {acct_code} was processed!" in caplog.text
            pp_accounts_abridged = Account.filter(
                erp_code=acct_code)  # TODO - make it so the Account.filter returns Account objects, not AccountList objects to save a request?
            pp_account_abridged: Account = Account.get(pp_accounts_abridged[0].id)
            pp_account_abridged.delete()

    def test_purchased_component_importer(self, caplog):
        import random
        partno = str(random.randint(1, 100000000000))
        with requests_mock.Mocker(real_http=True) as mock:
            mock.post("http://testapi.com/token/user", text='{"access_token": "blah"}', status_code=200)
            part_text = json.dumps(PART_RESPONSE).replace("replace_me", partno)
            mock.get("http://testapi.com/api/Parts", text="[]", status_code=200)
            mock.get(f"http://testapi.com/api/Parts?PartNumber={partno}", text=part_text, status_code=200)
            integration = Integration()
            """Create integration and register the customer processor to process orders"""
            from jobscope.importer.importer import JobscopePurchasedComponentImporter
            i = JobscopePurchasedComponentImporter(integration)
            i.run()
            assert "0 new purchased_components were found to import" in caplog.text
            i.run(partno)
            assert "Bulk processed 1 purchased components" in caplog.text
            i.run(partno)
            assert f"Purchased component {partno} was found in Paperless" in caplog.text
            pc: PurchasedComponent = PurchasedComponent.search(partno)[0]
            assert pc
            pc.delete()

    def test_failed_login(self, caplog):
        integration = Integration()
        """Create integration and register the customer processor to process orders"""
        from jobscope.exporter.exporter import JobscopeOrderExporter
        with requests_mock.Mocker(real_http=True) as mock:
            """Create integration and register the customer processor to process orders"""
            mock.post("http://testapi.com/token/user", text='{"access_token": "blah"}', status_code=400)
            with pytest.raises(ValueError):
                JobscopeOrderExporter(integration)

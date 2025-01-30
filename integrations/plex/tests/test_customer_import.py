# import standard libraries
import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))
from baseintegration.integration import Integration
from paperless.objects.customers import Account

import requests_mock


@pytest.fixture
def setup_importer_account():
    integration = Integration()
    from plex.importer.importer import PLEXAccountImporter
    i = PLEXAccountImporter(integration)
    return i


class TestCustomerProcessor:
    def test_customer_import(self, setup_importer_account):
        with requests_mock.Mocker(real_http=True) as mock:

            accounts = Account.filter(erp_code="Test PLEX Customer 1")
            for account in accounts:
                pp_account: Account = Account.get(id=account.id)
                pp_account.delete()
            """Create integration and register the customer processor to process orders"""
            json = '[{"id":"d0ecd99a-db01-4299-9b91-9f5088eccaed","code":"Test PLEX Customer 1","name":"Test PLEX Customer 1 name","status":"Active","type":"Automotive","note":"","supplierCode":"","otherCustomerCode":"53","rating":null,"industries":[],"defaultCarrierIds":[],"region":null,"businessType":"","category":null,"class":null,"catalog":null,"assignedToId":null,"assignedTo2Id":null,"assignedTo3Id":null,"assignedToGroup":null,"contactResourceId":null,"annualSalesMillions":null,"estimatedEmployees":"","phone":"","fax":"","email":"","trackingNoOnWeighScaleRequired":false,"multipleOrdersPerShipper":false,"estimatedAnnualSales":"","newShipperPerReleaseNo":false,"defaultBackOrder":null,"createdById":"92a38504-ec0c-4fa2-aeeb-073a123633f9","createdDate":"2014-04-16T19:25:00Z","modifiedById":"ee7a11ce-f234-4590-9d63-79162109db0e","modifiedDate":"2021-06-30T19:33:00Z"}]'
            mock.get("https://test.connect.plex.com/mdm/v1/customers",
                     text=json,
                     status_code=200)
            jsonc = '[{"id":"75d332bd-7d6d-45c7-a99a-83e9dacd2c53","customerId":"d0ecd99a-db01-4299-9b91-9f5088eccaed","firstName":"Test","lastName":"Supplier","supplierId":"null","phone":"","fax":"","mobilePhone":"","title":"Test Test","note":"","email":"test+testplex@paperlessparts.com","companyName":"","officeAddress":"","homeAddress":"","private":0,"description":"","birthDate":"null","url":"","sortOrder":22,"type":"Customer","associatedWithId":"a7db7d11-d162-4193-be8d-255d5c013099","modifiedById":"a7db7d11-d162-4193-be8d-255d5c013099","modifiedDate":"2014-08-20T16:36:00Z","createdById":"a7db7d11-d162-4193-be8d-255d5c013099","createdDate":"2014-08-20T16:36:05.253Z"}]'
            mock.get("https://test.connect.plex.com/mdm/v1/contacts",
                     text=jsonc,
                     status_code=200)
            jsona = '[{"id": "b09015e9-9fc3-4692-b831-20f3aeed2ebf","code": "Rockwall","note": "Rockwall Location","quoteTo": true,"shipTo": true,"billTo": false,"billToAddressId": "031829d7-7ca4-455b-9855-77ba1cc36161","remitTo": true,"thirdPartyShipTo": false,"thirdPartyShipToAddressId": null,"pool": false,"poolAddressId": null,"oldCustomerNo": "","active": true,"phone": "713.445.9491","fax": "","email": "customer@testcustomer.com","name": "","address": "145 Discovery Way","city": "Rockwall","state": "TX","zip": "73840","country": "USA","region": null,"county": "","shippingInstructions": "","ignoreTransitOnWeekends": false,"transportationLeadTime": 0,"defaultCarrierIds": [],"truckType": null,"salesTaxExempt": false,"salespersonId": null,"statementAddressId": null,"freightTerms": null,"insideSalespersonId": null,"defaultShipFrom": null,"freightBillTo": false,"freightBillToAddressId": null,"catalog": null,"soldTo": false,"dunsNo": "","commercialInvoiceVatNo": "","terms": null,"template": false,"incoTerms": null,"negotiatedPlace": "","backOrder": null,"createdById": "2bf93e17-57de-4cf5-b231-812e753e0801","createdDate": "2014-02-05T19:02:32.55Z","modifiedById": "a7db7d11-d162-4193-be8d-255d5c013099","modifiedDate": "2014-08-20T16:39:21.653Z"  },  {"id": "031829d7-7ca4-455b-9855-77ba1cc36161","code": "Billing","note": "test","quoteTo": false,"shipTo": false,"billTo": true,"billToAddressId": null,"remitTo": false,"thirdPartyShipTo": false,"thirdPartyShipToAddressId": null,"pool": false,"poolAddressId": null,"oldCustomerNo": "","active": true,"phone": "","fax": "","email": "","name": "","address": "","city": "","state": "","zip": "","country": "USA","region": null,"county": "","shippingInstructions": "","ignoreTransitOnWeekends": false,"transportationLeadTime": 0,"defaultCarrierIds": [],"truckType": null,"salesTaxExempt": false,"salespersonId": null,"statementAddressId": null,"freightTerms": null,"insideSalespersonId": null,"defaultShipFrom": null,"freightBillTo": false,"freightBillToAddressId": null,"catalog": null,"soldTo": false,"dunsNo": "","commercialInvoiceVatNo": "","terms": null,"template": false,"incoTerms": null,"negotiatedPlace": "","backOrder": null,"createdById": "a7db7d11-d162-4193-be8d-255d5c013099","createdDate": "2014-08-20T16:38:49.347Z","modifiedById": null,"modifiedDate": null  },  {"id": "dff1a9a1-6e46-4d75-aeb2-1be9a353ce6f","code": "HQ","note": "TEST","quoteTo": false,"shipTo": true,"billTo": false,"billToAddressId": null,"remitTo": false,"thirdPartyShipTo": false,"thirdPartyShipToAddressId": null,"pool": false,"poolAddressId": null,"oldCustomerNo": "","active": true,"phone": "","fax": "","email": "","name": "","address": "1234 test test St","city": "test","state": "MI","zip": "48084","country": "USA","region": null,"county": "","shippingInstructions": "","ignoreTransitOnWeekends": false,"transportationLeadTime": 0,"defaultCarrierIds": [],"truckType": null,"salesTaxExempt": false,"salespersonId": null,"statementAddressId": null,"freightTerms": null,"insideSalespersonId": null,"defaultShipFrom": null,"freightBillTo": false,"freightBillToAddressId": null,"catalog": null,"soldTo": false,"dunsNo": "","commercialInvoiceVatNo": "","terms": null,"template": false,"incoTerms": null,"negotiatedPlace": "","backOrder": null,"createdById": "85ba75e6-c48a-49de-ba19-ae1bfa166e4c","createdDate": "2014-08-20T17:17:21.947Z","modifiedById": "85ba75e6-c48a-49de-ba19-ae1bfa166e4c","modifiedDate": "2014-08-20T17:17:44.067Z"  },  {"id": "031829d7-7cb4-455b-9855-77ba1cc36351","code": "Billing","note": "test","quoteTo": false,"shipTo": false,"billTo": true,"billToAddressId": null,"remitTo": false,"thirdPartyShipTo": false,"thirdPartyShipToAddressId": null,"pool": false,"poolAddressId": null,"oldCustomerNo": "","active": true,"phone": "","fax": "","email": "","name": "","address": "1234 test St","city": "Troy","state": "MI","zip": "48084","country": "USA","region": null,"county": "","shippingInstructions": "","ignoreTransitOnWeekends": false,"transportationLeadTime": 0,"defaultCarrierIds": [],"truckType": null,"salesTaxExempt": false,"salespersonId": null,"statementAddressId": null,"freightTerms": null,"insideSalespersonId": null,"defaultShipFrom": null,"freightBillTo": false,"freightBillToAddressId": null,"catalog": null,"soldTo": false,"dunsNo": "","commercialInvoiceVatNo": "","terms": null,"template": false,"incoTerms": null,"negotiatedPlace": "","backOrder": null,"createdById": "a7db7d11-d162-4193-be8d-255d5c013099","createdDate": "2014-08-20T16:38:49.347Z","modifiedById": null,"modifiedDate": null  },  {"id": "b09015e9-9fc6-4542-a861-20f3aeed2ebf","code": "Rockwall","note": "Rockwall Location","quoteTo": true,"shipTo": true,"billTo": false,"billToAddressId": "031829d7-7ca4-455b-9855-77ba1cc36161","remitTo": true,"thirdPartyShipTo": false,"thirdPartyShipToAddressId": null,"pool": false,"poolAddressId": null,"oldCustomerNo": "","active": true,"phone": "713.445.9491","fax": "","email": "customer@testcustomer.com","name": "","address": "","city": "","state": "","zip": "","country": "USA","region": null,"county": "","shippingInstructions": "","ignoreTransitOnWeekends": false,"transportationLeadTime": 0,"defaultCarrierIds": [],"truckType": null,"salesTaxExempt": false,"salespersonId": null,"statementAddressId": null,"freightTerms": null,"insideSalespersonId": null,"defaultShipFrom": null,"freightBillTo": false,"freightBillToAddressId": null,"catalog": null,"soldTo": false,"dunsNo": "","commercialInvoiceVatNo": "","terms": null,"template": false,"incoTerms": null,"negotiatedPlace": "","backOrder": null,"createdById": "2bf93e17-57de-4cf5-b231-812e753e0801","createdDate": "2014-02-05T19:02:32.55Z","modifiedById": "a7db7d11-d162-4193-be8d-255d5c013099","modifiedDate": "2014-08-20T16:39:21.653Z"  },  {"id": "b09015e9-9fc3-4692-b831-20f3aeed2ebf","code": "Rockwall","note": "Rockwall Location","quoteTo": false,"shipTo": false,"billTo": false,"billToAddressId": "031829d7-7ca4-455b-9855-77ba1cc36161","remitTo": true,"thirdPartyShipTo": false,"thirdPartyShipToAddressId": null,"pool": false,"poolAddressId": null,"oldCustomerNo": "","active": true,"phone": "713.445.9491","fax": "","email": "customer@testcustomer.com","name": "","address": "145 Discovery Way","city": "Rockwall","state": "TX","zip": "73840","country": "USA","region": null,"county": "","shippingInstructions": "","ignoreTransitOnWeekends": false,"transportationLeadTime": 0,"defaultCarrierIds": [],"truckType": null,"salesTaxExempt": false,"salespersonId": null,"statementAddressId": null,"freightTerms": null,"insideSalespersonId": null,"defaultShipFrom": null,"freightBillTo": false,"freightBillToAddressId": null,"catalog": null,"soldTo": true,"dunsNo": "","commercialInvoiceVatNo": "","terms": null,"template": false,"incoTerms": null,"negotiatedPlace": "","backOrder": null,"createdById": "2bf93e17-57de-4cf5-b231-812e753e0801","createdDate": "2014-02-05T19:02:32.55Z","modifiedById": "a7db7d11-d162-4193-be8d-255d5c013099","modifiedDate": "2014-08-20T16:39:21.653Z" }, {"id": "b09015e9-9fc3-4692-b831-20f3aeed2ebf","code": "Rockwall","note": "Rockwall Location","quoteTo": false,"shipTo": false,"billTo": false,"billToAddressId": "031829d7-7ca4-455b-9855-77ba1cc36161","remitTo": true,"thirdPartyShipTo": false,"thirdPartyShipToAddressId": null,"pool": false,"poolAddressId": null,"oldCustomerNo": "","active": true,"phone": "713.445.9491","fax": "","email": "customer@testcustomer.com","name": "","address": "","city": "","state": "","zip": "","country": "USA","region": null,"county": "","shippingInstructions": "","ignoreTransitOnWeekends": false,"transportationLeadTime": 0,"defaultCarrierIds": [],"truckType": null,"salesTaxExempt": false,"salespersonId": null,"statementAddressId": null,"freightTerms": null,"insideSalespersonId": null,"defaultShipFrom": null,"freightBillTo": false,"freightBillToAddressId": null,"catalog": null,"soldTo": true,"dunsNo": "","commercialInvoiceVatNo": "","terms": null,"template": false,"incoTerms": null,"negotiatedPlace": "","backOrder": null,"createdById": "2bf93e17-57de-4cf5-b231-812e753e0801","createdDate": "2014-02-05T19:02:32.55Z","modifiedById": "a7db7d11-d162-4193-be8d-255d5c013099","modifiedDate": "2014-08-20T16:39:21.653Z" }]'
            mock.get("https://test.connect.plex.com/mdm/v1/customers/d0ecd99a-db01-4299-9b91-9f5088eccaed/addresses",
                     text=jsona,
                     status_code=200)
            setup_importer_account._process_account(account_id="Test PLEX Customer 1")
            account = Account.filter(erp_code="Test PLEX Customer 1")
            pp_account: Account = Account.get(id=account[0].id)
            pp_account.erp_code = ''
            pp_account.update()
            setup_importer_account._process_account(account_id='Test PLEX Customer 1')
            setup_importer_account._process_account(account_id='Test PLEX Customer 1')
            pp_account.delete()

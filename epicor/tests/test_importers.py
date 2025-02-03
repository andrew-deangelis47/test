# import standard libraries
import os
from epicor.importer.importer import EpicorAccountImporter, EpicorPurchasedComponentImporter, EpicorMaterialImporter, \
    EpicorVendorImporter, EpicorWorkCenterImporter
from epicor.importer.repeat_work_importer import EpicorRepeatWorkImporter
# append to path
import sys
import requests_mock
import json
import re
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))
from baseintegration.integration import Integration


def load_file(file_name: str, wrap_value=True) -> json:
    with open(os.path.join(os.path.dirname(__file__), f"data/{file_name}"), 'r') as f:
        if wrap_value:
            return json.dumps({'value': [json.load(f)]})
        else:
            return json.dumps(json.load(f))


@pytest.fixture
def setup_material_importer() -> EpicorMaterialImporter:
    integration = Integration()
    from epicor.importer.importer import EpicorMaterialImporter
    i = EpicorMaterialImporter(integration)
    return i


def register_mocks(mocker):
    customer_matcher = re.compile("Erp.BO.CustomerSvc/Customers")
    salesperson_matcher = re.compile("Erp.BO.SalesRepSvc/SalesReps")
    terms_matcher = re.compile("Erp.BO.TermsSvc/Terms")
    contact_matcher = re.compile("Erp.BO.CustCntSvc/CustCnts")
    ship_to_matcher = re.compile("Erp.BO.ShipToSvc/ShipToes")
    vendor_matcher = re.compile("Erp.BO.VendorSvc/Vendors")
    part_matcher = re.compile("Erp.BO.PartSvc/Parts")
    op_matcher = re.compile("Erp.BO.OpMasterSvc/OpMasters")
    op_detail_matcher = re.compile("Erp.BO.OpMasterSvc/OpMasDtls")
    part_cost_matcher = re.compile("Erp.BO.PartCostSearchSvc/PartCostSearches")
    resource_group_matcher = re.compile("Erp.BO.ResourceGroupSvc/ResourceGroups")
    resource_matcher = re.compile("Erp.BO.ResourceSvc/Resources")

    # register mockers
    mocker.get(customer_matcher, text=load_file('customer.json'), status_code=200)
    mocker.get(salesperson_matcher, text=load_file('salesperson.json'), status_code=200)
    mocker.get(terms_matcher, text=load_file('terms.json'), status_code=200)
    mocker.get(part_matcher, text=load_file("create_part.json"), status_code=200)
    mocker.get(part_cost_matcher, text=load_file("part_cost_search.json"), status_code=200)
    mocker.get(contact_matcher, text=load_file('contact.json'), status_code=200)
    mocker.get(ship_to_matcher, text=load_file('ship_to.json'), status_code=200)
    mocker.get(vendor_matcher, text=load_file('vendor.json'), status_code=200)
    mocker.get(op_matcher, text=load_file('operation.json'), status_code=200)
    mocker.get(op_detail_matcher, text=load_file('op_details.json'), status_code=200)
    mocker.get(resource_matcher, text=load_file('resource.json'), status_code=200)
    mocker.get(resource_group_matcher, text=load_file('resource_group.json'), status_code=200)


empty_data = json.dumps({'value': []})


def url_is_in_request_history(url, method, mocker):
    for req in mocker.request_history:
        if url in str(req.url) and method == str(req.method):
            return True
    else:
        return False


class TestAccountImporter:

    def test_import_account(self, caplog):
        integration = Integration()
        account_importer = EpicorAccountImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            account_importer.run("10")
            assert "Processing Epicor Customer ID: 10" in caplog.text
            assert url_is_in_request_history("Erp.BO.CustomerSvc/Customers", "GET", m)
            assert url_is_in_request_history("Erp.BO.SalesRepSvc/SalesReps", "GET", m)
            assert url_is_in_request_history("Erp.BO.TermsSvc/Terms", "GET", m)
            assert "Attempting to sync payment terms" in caplog.text

    def test_import_purchased_component(self, caplog):
        integration = Integration()
        purchased_component_importer = EpicorPurchasedComponentImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            purchased_component_importer.run("200-123")
            assert "Processing purchased component 200-123" in caplog.text
            assert url_is_in_request_history("Erp.BO.PartSvc/Parts", "GET", m)
            purchased_component_importer.run("040821")
            assert "Processing purchased component 040821" in caplog.text
            assert purchased_component_importer._bulk_process_purchased_component(["040821"])

    def test_import_raw_material(self, setup_material_importer, caplog):
        integration = Integration()
        material_importer = EpicorMaterialImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_material_importer.erp_config.should_update_null_dates = True
            material_importer.run("AL6061")
            assert "Processing material AL6061" in caplog.text
            assert url_is_in_request_history("Erp.BO.PartSvc/Parts", "GET", m)
            assert url_is_in_request_history("Erp.BO.PartCostSearchSvc/PartCostSearches", "GET", m)
            assert "Processed epicor-material-bulk-upload-count-1 successfully" in caplog.text
            assert "Processed Material id: AL6061" in caplog.text
            assert material_importer._bulk_process_material(["AL6061"])

    def test_import_vendor(self, caplog):
        integration = Integration()
        vendor_importer = EpicorVendorImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            vendor_importer.run("FINISH")
            assert "Processing vendor FINISH" in caplog.text
            assert url_is_in_request_history("Erp.BO.VendorSvc/Vendors", "GET", m)
            assert "Processed vendor id: FINISH" in caplog.text
            assert vendor_importer._bulk_process_vendor(["FINISH"])

    def test_import_work_center(self, caplog):
        integration = Integration()
        work_center_importer = EpicorWorkCenterImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            work_center_importer.run("LATHE::operation")
            assert "Processing operation LATHE" in caplog.text
            assert url_is_in_request_history("Erp.BO.OpMasterSvc/OpMaster", "GET", m)
            assert url_is_in_request_history("Erp.BO.OpMasterSvc/OpMaster", "GET", m)
            work_center_importer.run("MILL::resource_group")
            assert "Processing resource group MILL" in caplog.text
            assert url_is_in_request_history("Erp.BO.ResourceGroupSvc/ResourceGroups", "GET", m)
            work_center_importer.run("JACK::resource")
            assert "Processing resource JACK" in caplog.text
            assert url_is_in_request_history("Erp.BO.ResourceSvc/Resources", "GET", m)
            assert work_center_importer._bulk_process_work_center(["LATHE::operation", "MILL::resource_group",
                                                                   "JACK::resource"])

    def test_repeat_work_configuration(self, caplog):
        integration = Integration()
        work_center_importer = EpicorRepeatWorkImporter(integration)
        work_center_importer.erp_config.company_name = "TEST"
        work_center_importer.erp_config.import_objects_newer_than = "1970-01-01T00:00:00Z"
        work_center_importer.erp_config.is_post_enabled = False
        work_center_importer.erp_config.page_size = 25
        work_center_importer.erp_config.job_id_count_filter_limit = 25
        work_center_importer.erp_config.quote_id_count_filter_limit = 25
        work_center_importer.erp_config.ewb_id_count_filter_limit = 25

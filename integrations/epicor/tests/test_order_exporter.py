# import standard libraries
import os
from epicor.exporter.exporter import EpicorOrderExporter
import pytest

# append to path
import sys
import requests_mock
import json
import re

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../baseintegration"))
from baseintegration.integration import Integration
from baseintegration.utils.test_utils import get_order
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


class MockHelper:
    mock_data = {}

    def load_model(self, file_name):
        with open(os.path.join(os.path.dirname(__file__), f"data/{file_name}"), 'r') as f:
            self.mock_data = json.load(f)

    def dump_model(self):
        return json.dumps(self.mock_data)


@pytest.fixture
def setup_order_exporter() -> EpicorOrderExporter:
    integration = Integration()
    from epicor.exporter.exporter import EpicorOrderExporter
    i = EpicorOrderExporter(integration)
    return i


def load_file(file_name: str, wrap_value=True) -> json:
    with open(os.path.join(os.path.dirname(__file__), f"data/{file_name}"), 'r') as f:
        if wrap_value:
            return json.dumps({'value': [json.load(f)]})
        else:
            return json.dumps(json.load(f))


def register_mocks(mocker):
    part_matcher = re.compile("Erp.BO.PartSvc/Parts")
    part_rev_matcher = re.compile("Erp.BO.PartSvc/PartRevs")
    quote_matcher = re.compile("Erp.BO.QuoteSvc/Quotes")
    quote_details_matcher = re.compile("Erp.BO.QuoteSvc/QuoteDtls")
    quote_quantities_matcher = re.compile("Erp.BO.QuoteSvc/QuoteQties")
    quote_op_matcher = re.compile("Erp.BO.QuoteAsmSvc/QuoteOprs")
    quote_op_detail_matcher = re.compile("Erp.BO.QuoteAsmSvc/QuoteOpDtls")
    quote_assembly_matcher = re.compile("Erp.BO.QuoteAsmSvc/QuoteAsms")
    operation_matcher = re.compile("Erp.BO.OpMasterSvc/OpMasters")
    quote_materials_matcher = re.compile("Erp.BO.QuoteAsmSvc/QuoteMtls")
    quote_contacts_matcher = re.compile("Erp.BO.QuoteSvc/QuoteCnts")
    operation_subcontract_vendor = re.compile("Erp.BO.VendorSvc/Vendors")
    salesperson = re.compile("Erp.BO.SalesRepSvc/SalesRep")
    misc_charge = re.compile("Erp.BO.MiscChrgSvc/MiscChrgs")
    quote_misc_charge = re.compile('Erp.BO.QuoteSvc/QuoteMscs')

    mocker.get(part_matcher, text="{}", status_code=404)
    mocker.post(part_matcher, text=load_file("create_part.json", False), status_code=201)
    mocker.get(part_rev_matcher, text="{}", status_code=404)
    mocker.get(operation_subcontract_vendor, text=load_file("get_vendor.json", False), status_code=200)
    mocker.post(part_rev_matcher, text=load_file("create_part_rev_response.json", False), status_code=201)
    mocker.post(quote_matcher, text=load_file("create_quote.json", False), status_code=201)
    mocker.post(quote_details_matcher, text=load_file("create_quote_detail.json", False), status_code=201)
    mocker.patch(quote_details_matcher, text=load_file("create_quote_detail.json", False), status_code=201)
    mocker.post(quote_quantities_matcher, text=load_file("create_quote_quantities.json", False), status_code=201)
    mocker.post(quote_op_matcher, text=load_file("create_quote_op.json", False), status_code=201)
    mocker.patch(quote_op_matcher, text=load_file("create_quote_op.json", False), status_code=201)
    mocker.patch(quote_op_detail_matcher, text=load_file("create_quote_op.json", False), status_code=201)
    mocker.get(quote_assembly_matcher, text=load_file("get_quote_assembly.json", False), status_code=200)
    mocker.post(quote_assembly_matcher, text=load_file("create_quote_assembly.json", False), status_code=201)
    mocker.get(operation_matcher, text=load_file("operation.json"), status_code=200)
    mocker.get(quote_materials_matcher, text=load_file("quote_material.json", False), status_code=200)
    mocker.post(quote_materials_matcher, text=load_file("create_quote_materials.json", False), status_code=200)
    mocker.post(quote_contacts_matcher, text=load_file("create_quote_contact.json", False), status_code=200)
    mocker.get(salesperson, text=load_file("get_salesperson_response.json", False), status_code=200)
    mocker.get(misc_charge, text=load_file("get_misc_charge_response.json", False), status_code=200)
    mocker.post(misc_charge, text=load_file("create_misc_charge.json", False), status_code=200)
    mocker.post(quote_misc_charge, text=load_file("create_quote_misc_charge.json", False), status_code=200)

    # register non regex matchers
    mocker.get(
        "/EpicorERPTest/api/v2/odata/ABC/Erp.BO.CustomerSvc/Customers",
        text=load_file('customer.json'), status_code=200)
    mocker.post(
        "/EpicorERPTest/api/v2/odata/ABC/Erp.BO.CustomerSvc/Customers",
        text=load_file('customer.json', False), status_code=200)
    mocker.get(
        "/EpicorERPTest/api/v2/odata/ABC/Erp.BO.TermsSvc/Terms",
        text=load_file('terms.json'), status_code=200)
    mocker.get(
        "/EpicorERPTest/api/v2/odata/ABC/Erp.BO.CustCntSvc/CustCnts",
        text=load_file('contact.json'), status_code=200)
    mocker.post(
        "/EpicorERPTest/api/v2/odata/ABC/Erp.BO.CustCntSvc/CustCnts",
        text=load_file('contact.json', False), status_code=200)
    mocker.get(
        "/EpicorERPTest/api/v2/odata/ABC/Erp.BO.ShipToSvc/ShipToes",
        text=load_file('ship_to.json'), status_code=200)
    mocker.post(
        "/EpicorERPTest/api/v2/odata/ABC/Erp.BO.ShipToSvc/ShipToes",
        text=load_file('ship_to.json', False), status_code=200)
    mocker.get(
        "/EpicorERPTest/api/v2/odata/ABC/Erp.BO.CountrySvc/Countries",
        text=load_file('country.json'), status_code=200)


empty_data = json.dumps({'value': []})


def url_is_in_request_history(url, method, mocker):
    for req in mocker.request_history:
        if url in str(req.url) and method == str(req.method):
            return True
    else:
        return False


def url_is_not_in_request_history(url, method, mocker):
    for req in mocker.request_history:
        if url in str(req.url) and method == str(req.method):
            return False
        else:
            return True


class TestEpicorCustomerProcessing:
    def test_customer_found(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter._process_order(get_order(133))
            assert url_is_in_request_history("CustomerSvc/Customers", "GET", m)
            assert "Customer was found" in caplog.text

    def test_customer_not_found_cancel_order(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            m.get("/EpicorERPTest/api/v2/odata/ABC/Erp.BO.CustomerSvc/Customers",
                  text=empty_data, status_code=200)
            setup_order_exporter.erp_config.should_create_customer = False
            with pytest.raises(CancelledIntegrationActionException):
                setup_order_exporter._process_order(get_order(133))
            assert url_is_in_request_history("CustomerSvc/Customers", "GET", m)
            assert "Customer was not found" in caplog.text
            assert not url_is_in_request_history("CustomerSvc/Customers", "POST", m)

    def test_customer_not_found_create_customer(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            m.get("/EpicorERPTest/api/v2/odata/ABC/Erp.BO.CustomerSvc/Customers",
                  text=empty_data, status_code=200)
            setup_order_exporter.erp_config.should_create_customer = True
            setup_order_exporter._process_order(get_order(133))
            assert url_is_in_request_history("CustomerSvc/Customers", "GET", m)
            assert "Customer was not found" in caplog.text
            assert "Creating customer" in caplog.text
            assert url_is_in_request_history("CustomerSvc/Customers", "POST", m)

    def test_customer_default_not_found(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            m.get("/EpicorERPTest/api/v2/odata/ABC/Erp.BO.CustomerSvc/Customers",
                  text=empty_data, status_code=200)
            setup_order_exporter.erp_config.should_create_customer = False
            setup_order_exporter.erp_config.default_customer_id = 'Cust123'
            with pytest.raises(CancelledIntegrationActionException):
                setup_order_exporter._process_order(get_order(133))
            assert url_is_in_request_history("CustomerSvc/Customers", "GET", m)
            assert "Customer was not found" in caplog.text
            assert "Using default customer" in caplog.text
            assert not url_is_in_request_history("CustomerSvc/Customers", "POST", m)

    def test_contact_found(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter._process_order(get_order(133))
            assert url_is_in_request_history("CustCntSvc/CustCnts", "GET", m)
            assert "Contact was found" in caplog.text

    def test_contact_not_found_create_contact(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            m.get("/EpicorERPTest/api/v2/odata/ABC/Erp.BO.CustCntSvc/CustCnts",
                  text=empty_data, status_code=200)
            setup_order_exporter.erp_config.should_create_contact = True
            setup_order_exporter._process_order(get_order(133))
            assert url_is_in_request_history("CustCntSvc/CustCnts", "GET", m)
            assert "Contact was not found" in caplog.text
            assert "Creating contact" in caplog.text
            assert url_is_in_request_history("CustCntSvc/CustCnts", "POST", m)

    def test_contact_not_found_skip(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            m.get("/EpicorERPTest/api/v2/odata/ABC/Erp.BO.CustCntSvc/CustCnts",
                  text=empty_data, status_code=200)
            setup_order_exporter.erp_config.should_create_contact = False
            setup_order_exporter._process_order(get_order(133))
            assert url_is_in_request_history("CustCntSvc/CustCnts", "GET", m)
            assert "Contact was not found" in caplog.text
            assert "Skipping the creation of contact" in caplog.text
            assert not url_is_in_request_history("CustCntSvc/CustCnts", "POST", m)

    def test_contact_default_not_found(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            m.get("/EpicorERPTest/api/v2/odata/ABC/Erp.BO.CustCntSvc/CustCnts",
                  text=empty_data, status_code=200)
            setup_order_exporter.erp_config.should_create_contact = False
            setup_order_exporter.erp_config.default_contact_email = 'contact123@gmail.com'
            setup_order_exporter._process_order(get_order(133))
            assert url_is_in_request_history("CustCntSvc/CustCnts", "GET", m)
            assert "Contact was not found" in caplog.text
            assert "Using default contact" in caplog.text
            assert "Skipping the creation of contact" in caplog.text
            assert not url_is_in_request_history("CustCntSvc/CustCnts", "POST", m)

    def test_shipping_address_found(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter._process_order(get_order(136))
            assert url_is_in_request_history("ShipToSvc/ShipToes", "GET", m)
            assert "Shipping address was found" in caplog.text

    def test_create_shipping_address(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            m.get("/EpicorERPTest/api/v2/odata/ABC/Erp.BO.ShipToSvc/ShipToes",
                  text=empty_data, status_code=200)
            setup_order_exporter.erp_config.should_create_shipping_address = True
            setup_order_exporter._process_order(get_order(136))
            assert url_is_in_request_history("ShipToSvc/ShipToes", "GET", m)
            assert "Shipping address was not found" in caplog.text
            assert "Creating shipping address" in caplog.text
            assert url_is_in_request_history("ShipToSvc/ShipToes", "POST", m)

    def test_skip_shipping_address(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            m.get("/EpicorERPTest/api/v2/odata/ABC/Erp.BO.ShipToSvc/ShipToes",
                  text=empty_data, status_code=200)
            setup_order_exporter.erp_config.should_create_shipping_address = False
            setup_order_exporter._process_order(get_order(136))
            assert url_is_in_request_history("ShipToSvc/ShipToes", "GET", m)
            assert "Shipping address was not found" in caplog.text
            assert "Skipping the creation of shipping address" in caplog.text
            assert not url_is_in_request_history("ShipToSvc/ShipToes", "POST", m)

    def test_create_part_create_revision(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter._process_order(get_order(150))
            assert "Creating root component part." in caplog.text
            assert "Root component is going into mfg component list, part number" in caplog.text
            assert "Creating purchased components for root component:" in caplog.text
            assert "Creating raw materials for root component:" in caplog.text
            assert "Attempting to remove duplicate part number." in caplog.text
            assert "Checking for valid part number length." in caplog.text
            assert "Part DUPLICATE-PART does not yet exist" in caplog.text
            assert "Creating new revision" in caplog.text
            assert url_is_in_request_history("Erp.BO.PartSvc/Parts", "POST", m)
            assert url_is_in_request_history("Erp.BO.PartSvc/PartRevs", "POST", m)

    def test_get_part_get_revision(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            part_matcher = re.compile("Erp.BO.PartSvc/Parts")
            part_rev_matcher = re.compile("Erp.BO.PartSvc/PartRevs")
            m.get(part_matcher, text=load_file("get_part_number_040821.json", False), status_code=200)
            m.get(part_rev_matcher, text=load_file("get_part_revision.json", False), status_code=200)
            setup_order_exporter._process_order(get_order(133))
            assert "part found" in caplog.text
            assert "Attempting to get or create a part revision." in caplog.text
            assert not url_is_in_request_history("Erp.BO.PartSvc/Parts", "POST", m)
            assert url_is_in_request_history("Erp.BO.PartSvc/Parts", "GET", m)
            assert url_is_in_request_history("Erp.BO.PartSvc/PartRevs", "GET", m)

    def test_get_part_create_revision(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            part_matcher = re.compile("Erp.BO.PartSvc/Parts")
            m.get(part_matcher, text=load_file("get_part_number_040821.json", False), status_code=200)
            setup_order_exporter._process_order(get_order(150))
            assert "Attempting to get or create a part revision." in caplog.text
            assert "part found" in caplog.text
            assert "Creating new revision" in caplog.text
            assert not url_is_in_request_history("Erp.BO.PartSvc/Parts", "POST", m)
            assert url_is_in_request_history("Erp.BO.PartSvc/PartRevs", "POST", m)

    def test_null_revision(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter._process_order(get_order(133))
            assert "Using default part revision" in caplog.text
            assert url_is_in_request_history("Erp.BO.PartSvc/PartRevs", "POST", m) is True

    def test_informational_material_op(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter.erp_config.pp_mat_id_variable = "No match"
            setup_order_exporter._process_order(get_order(150))
            assert "Attempting to process all quote operations" in caplog.text
            assert "Ignoring this operation - operation id indicates: " in caplog.text

    def test_create_quote(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter._process_order(get_order(153))
            # change config option to ensure customer should be created
            assert "Instantiated process method on the QuoteHeaderProcessor" in caplog.text
            assert "Attempting to create Epicor Quote Header" in caplog.text
            assert "Created quote header" in caplog.text
            assert "Created quote item: 0 - 1" in caplog.text
            assert "Getting lead time and lead time units for line item." in caplog.text
            assert url_is_in_request_history("Erp.BO.QuoteSvc/Quotes", "POST", m)
            assert url_is_in_request_history("Erp.BO.QuoteSvc/QuoteDtls", "POST", m)
            assert url_is_in_request_history("Erp.BO.QuoteSvc/QuoteQties", "POST", m)
            assert url_is_in_request_history("Erp.BO.QuoteAsmSvc/QuoteOprs", "POST", m)

    def test_get_salesperson(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter._process_order(get_order(153))
            assert "Attempting to get a valid sales rep code from the Paperless salesperson." in caplog.text
            assert not url_is_in_request_history("Erp.BO.SalesRepSvc/SalesRep", "GET", m)
            assert "Returning default sales rep code of 1" in caplog.text

    def test_default_op_code(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter.erp_config.pp_op_id_variable = "ABC"
            setup_order_exporter._process_order(get_order(133))
            assert "Attempting to get operation ID from operation variable: ABC" in caplog.text
            assert url_is_in_request_history("Erp.BO.QuoteAsmSvc/QuoteOprs", "POST", m)

    def test_create_quote_material(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter._process_order(get_order(150))
            assert "Adding quote materials to quote." in caplog.text
            assert "processing PP material operations for part number" in caplog.text
            assert "processing PP purchased components for part number:" in caplog.text
            assert "Attempting to get raw material quantity per value" in caplog.text
            assert "Attempting to get raw material unit price" in caplog.text
            assert "Attempting to get cost unit of measure" in caplog.text
            assert "Attempting to get material operation notes" in caplog.text
            assert "Attempting to get purchased component notes" in caplog.text
            assert "Attempting to get purchased component unit price" in caplog.text
            assert "Creating Epicor quote material from Paperless Parts Purchased Component" in caplog.text
            assert "Creating Epicor quote material from Paperless Parts Material Operation" in caplog.text
            assert "Attempting to get material supplier ID from operation:" in caplog.text
            assert "Attempting to get material lead time for operation:" in caplog.text
            assert url_is_in_request_history("Erp.BO.QuoteAsmSvc/QuoteMtls", "POST", m)
            setup_order_exporter.erp_config.should_create_raw_materials = False
            setup_order_exporter._process_order(get_order(150))
            assert "Creation of raw materials is disabled! Attempting to assign default part number." in caplog.text
            assert "No default part exists in Epicor for part number:" in caplog.text

    def test_create_quote_contact(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter._process_order(get_order(133))
            assert "Processing quote contact for order" in caplog.text
            assert "Created quote contact: " in caplog.text
            assert url_is_in_request_history("Erp.BO.QuoteSvc/QuoteCnts", "POST", m)

    def test_assign_subcontract_detail(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter._process_order(get_order(152))
            setup_order_exporter._integration.test_mode = False
            assert "Attempting to get subcontract information." in caplog.text
            assert "Attempting to get subcontract lead days." in caplog.text
            assert "Attempting to get subcontract unit cost." in caplog.text
            assert "Attempting to get subcontract min charge." in caplog.text
            assert url_is_in_request_history("Erp.BO.VendorSvc/Vendors", "GET", m)

    def test_no_create_reference_with_quote_number(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            # change config option to ensure PP quote number is not added to reference field
            setup_order_exporter.erp_config.should_populate_reference_with_pp_quote_num = False
            assert setup_order_exporter.erp_config.should_populate_reference_with_pp_quote_num is False
            setup_order_exporter._process_order(get_order(153))
            assert "Adding Paperless Parts quote number 134-4 to Epicor reference field." not in caplog.text

    def test_create_reference_with_quote_number(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            # change config option to ensure PP quote number is added to reference field
            setup_order_exporter.erp_config.should_populate_reference_with_pp_quote_num = True
            assert setup_order_exporter.erp_config.should_populate_reference_with_pp_quote_num is True
            setup_order_exporter._process_order(get_order(153))
            assert "Adding Paperless Parts quote number 134-4 to Epicor reference field." in caplog.text

    def test_no_add_part_viewer_url_to_quote_comments(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            # change config option to ensure part viewer URL is not added to quote comments
            setup_order_exporter.erp_config.should_add_pp_part_viewer_link_to_quote_comments = False
            assert setup_order_exporter.erp_config.should_add_pp_part_viewer_link_to_quote_comments is False
            setup_order_exporter._process_order(get_order(153))
            assert "Adding Paperless Parts Part Viewer URL to comments on quote detail: " \
                   "https://app.paperlessparts.com/parts/viewer/22122b3b-ce1c-4de1-8dc1-4648eb55ad3a" not in caplog.text

    def test_add_part_viewer_url_to_quote_comments(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            # change config option to ensure part viewer URL is not added to quote comments
            setup_order_exporter.erp_config.should_add_pp_part_viewer_link_to_quote_comments = True
            assert setup_order_exporter.erp_config.should_add_pp_part_viewer_link_to_quote_comments is True
            setup_order_exporter._process_order(get_order(153))
            assert "Adding Paperless Parts Part Viewer URL to comments on quote detail: " \
                   "https://app.paperlessparts.com/parts/viewer/22122b3b-ce1c-4de1-8dc1-4648eb55ad3a" in caplog.text

    def test_production_erp_config(self, setup_order_exporter):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter._integration.config_yaml["Exporters"] = {"orders": {}}
            setup_order_exporter._set_production_erp_config()
            assert setup_order_exporter.erp_config.verify_ssl_cert is True
            assert setup_order_exporter.erp_config.search_for_existing_customer is True
            assert setup_order_exporter.erp_config.should_add_private_pp_notes_to_quote_detail is False
            assert setup_order_exporter.erp_config.should_add_public_pp_notes_to_quote_detail is True
            assert setup_order_exporter.erp_config.should_populate_reference_with_pp_quote_num is False
            assert setup_order_exporter.erp_config.should_add_pp_part_viewer_link_to_quote_comments is False

    def test_create_new_epicor_misc_charge(self, setup_order_exporter, caplog):
        misc_charge = re.compile("Erp.BO.MiscChrgSvc/MiscChrgs")
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            m.get(misc_charge, text="{}", status_code=404)
            setup_order_exporter.erp_config.add_ons_should_create_new_misc_charges = True
            assert setup_order_exporter.erp_config.add_ons_should_create_new_misc_charges is True
            setup_order_exporter._process_order(get_order(153))  # This order has an Add On
            assert "Processing additional charge for order:" in caplog.text
            assert "Attempting to create new Epicor MiscCharge from Paperless Add On:" in caplog.text
            assert url_is_in_request_history('Erp.BO.MiscChrgSvc/MiscChrgs', "GET", m)
            assert url_is_in_request_history('Erp.BO.MiscChrgSvc/MiscChrgs', "POST", m)
            assert url_is_in_request_history('Erp.BO.QuoteSvc/QuoteMscs', "POST", m)

    def test_create_misc_charge_as_line_item(self, setup_order_exporter, caplog):
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter.erp_config.add_ons_should_create_line_items = True
            assert setup_order_exporter.erp_config.add_ons_should_create_line_items is True
            setup_order_exporter._process_order(get_order(153))  # This order has an Add On
            assert "Processing additional charge for order:" in caplog.text
            assert "Attempting to create line item from add on..." in caplog.text
            assert url_is_not_in_request_history('Erp.BO.MiscChrgSvc/MiscChrgs', "POST", m)
            assert url_is_not_in_request_history('Erp.BO.QuoteSvc/QuoteMscs', "POST", m)
            assert url_is_in_request_history('Erp.BO.QuoteSvc/QuoteDtls', "POST", m)
            assert url_is_in_request_history("Erp.BO.QuoteSvc/QuoteQties", "POST", m)

    def test_get_misc_charge_by_erp_code(self, setup_order_exporter, caplog):
        misc_charge = re.compile("Erp.BO.MiscChrgSvc/MiscChrgs")
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            setup_order_exporter.erp_config.add_ons_should_create_line_items = False
            assert setup_order_exporter.erp_config.add_ons_should_create_line_items is False
            # Order 167 has two add-ons: {name: 'FAI', erp_code: 'test'} and {name: 'NRE', erp_code: ''}
            mock_helper_get = MockHelper
            mock_helper_get.load_model(mock_helper_get, "get_misc_charge_response.json")
            mock_helper_get.mock_data["MiscCode"] = "test"
            m.get(misc_charge, text=mock_helper_get.dump_model(mock_helper_get), status_code=200)
            setup_order_exporter._process_order(get_order(180))
            assert "Searching for resource MiscChrgs with {'MiscCode': 'test'}" in caplog.text
            assert "Processing additional charge for order:" in caplog.text
            assert "Epicor resource MiscChrgs with {'MiscCode': 'test'} was found!"
            assert url_is_in_request_history('Erp.BO.QuoteSvc/QuoteMscs', "POST", m)
            mock_helper_get.mock_data["MiscCode"] = "NRE"
            m.get(misc_charge, text=mock_helper_get.dump_model(mock_helper_get), status_code=200)
            setup_order_exporter._process_order(get_order(180))
            assert "Searching for resource MiscChrgs with {'MiscCode': 'NRE'}" in caplog.text
            assert "Epicor resource MiscChrgs with {'MiscCode': 'NRE'} was found!"

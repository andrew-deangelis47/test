import unittest
from acumatica.importer.importer import AcumaticaMaterialImporter, AcumaticaVendorImporter, \
    AcumaticaWorkCenterImporter, AcumaticaAccountImporter, AcumaticaPurchasedComponentImporter, \
    AcumaticaOutsideServiceImporter
from baseintegration.integration import Integration
import os
import json
import re
import requests_mock
import acumatica.importer.importer as importer
from acumatica.client import AcumaticaClient
from acumatica.importer.processors.purchased_component import AcumaticaPurchasedComponentImportProcessor
from acumatica.api_models.acumatica_models import StockItem, DEFAULT_VERSION, MANUFACTURING_VERSION
from paperless.client import PaperlessClient


def loadfile(filename: str):
    with open(os.path.join(os.path.dirname(__file__), f"data/{filename}"), 'r') as f:
        return json.load(f)


def load_file(file_name: str, wrap_value=True) -> json:
    with open(os.path.join(os.path.dirname(__file__), f"data/{file_name}"), 'r') as f:
        if wrap_value:
            return json.dumps({'value': [json.load(f)]})
        else:
            return json.dumps(json.load(f))


def register_mocks(mocker):
    account_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/Customer")
    customer_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/Customer/C100001")
    customer_location_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/CustomerLocation")
    token_matcher = re.compile("identity/connect/token")
    stock_item_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/StockItem")
    vendor_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/Vendor")
    work_center_matcher = re.compile(f"entity/Manufacturing/{MANUFACTURING_VERSION}/WorkCenter")
    outside_service_matcher = re.compile(f"entity/Default/{MANUFACTURING_VERSION}/NonStockItem")
    contact_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/Contact")

    # register mockers
    mocker.get(account_matcher, json=loadfile('accounts.json'), status_code=200)
    mocker.get(customer_matcher, json=loadfile('customer.json'), status_code=200)
    mocker.get(customer_location_matcher, json=loadfile('customer_location.json'), status_code=200)
    mocker.post(token_matcher, json={"access_token": "abc", "refresh_token": "abc", "expires_in": 3600}, status_code=200)
    mocker.get(stock_item_matcher, json=loadfile('get_purchased_component.json'), status_code=200)
    mocker.get(vendor_matcher, json=loadfile('get_vendor.json'), status_code=200)
    mocker.get(work_center_matcher, json=loadfile('get_workcenter.json'), status_code=200)
    mocker.get(outside_service_matcher, json=loadfile('get_outside_services.json'), status_code=200)
    mocker.get(contact_matcher, json=loadfile('get_contacts.json'), status_code=200)


def register_alts(mocker):
    pc_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/StockItem")
    vendors_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/Vendor")
    wc_matcher = re.compile(f"entity/Manufacturing/{MANUFACTURING_VERSION}/WorkCenter")
    osv_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/NonStockItem")

    mocker.get(pc_matcher, json=loadfile('get_pcs.json'), status_code=200)
    mocker.get(vendors_matcher, json=loadfile('get_vendors.json'), status_code=200)
    mocker.get(wc_matcher, json=loadfile('get_wcs.json'), status_code=200)
    mocker.get(osv_matcher, json=loadfile('get_osvs.json'), status_code=200)


def url_is_in_request_history(url, method, mocker):
    for req in mocker.request_history:
        if url in str(req.url) and method == str(req.method):
            return True
    else:
        return False


class TestImporter:

    def test_import_account(self, caplog):
        integration = Integration()
        account_importer = AcumaticaAccountImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            account_importer.run('C100001')
            assert "Processing Acumatica Customer ID: C100001" in caplog.text
            assert url_is_in_request_history(f"entity/Default/{DEFAULT_VERSION}/Customer/", "GET", m)
            assert url_is_in_request_history(f"entity/Default/{DEFAULT_VERSION}/CustomerLocation", "GET", m)
            assert url_is_in_request_history(f"entity/Default/{DEFAULT_VERSION}/Contact", "GET", m)
            assert "Contact sync" in caplog.text

    def test_get_new_accounts(self, caplog):
        integration = Integration()
        AcumaticaClient(base_url="https://testapi.com")
        account_listener = importer.AcumaticaAccountImportListener(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            accounts = account_listener.get_new()
            assert type(accounts) == list

    def test_import_purchased_component(self, caplog):
        integration = Integration()
        pc_importer = AcumaticaPurchasedComponentImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            pc_importer.run('AKM1-420-260')
            assert "Processing purchased component AKM1-420-260" in caplog.text
            assert url_is_in_request_history(f"entity/Default/{DEFAULT_VERSION}/StockItem", "GET", m)

    def test_get_new_pcs(self, caplog):
        integration = Integration()
        AcumaticaClient(base_url="https://testapi.com")
        pc_listener = importer.AcumaticaPurchasedComponentImportListener(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_alts(m)
            pcs = pc_listener.get_new()
            assert type(pcs) == list

    def test_import_raw_material(self, caplog):
        integration = Integration()
        material_importer = AcumaticaMaterialImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            material_importer.run('AKM1-420-260')
            assert "Processing material AKM1-420-260" in caplog.text
            assert url_is_in_request_history(f"entity/Default/{DEFAULT_VERSION}/StockItem", "GET", m)

    def test_get_new_materials(self, caplog):
        integration = Integration()
        AcumaticaClient(base_url="https://testapi.com")
        mat_listener = importer.AcumaticaRawMaterialImportListener(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_alts(m)
            mats = mat_listener.get_new()
            assert type(mats) == list

    def test_import_vendor(self, caplog):
        integration = Integration()
        vendor_importer = AcumaticaVendorImporter(integration)
        vendor_importer.check_custom_table_exists()
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            vendor_importer.run('V100001')
            assert "Processing vendor V100001" in caplog.text
            assert url_is_in_request_history(f"entity/Default/{DEFAULT_VERSION}/Vendor", "GET", m)
            assert "Processed vendor id: V100001" in caplog.text

    def test_get_new_vendors(self, caplog):
        integration = Integration()
        AcumaticaClient(base_url="https://testapi.com")
        vendor_listener = importer.AcumaticaVendorImportListener(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_alts(m)
            vendors = vendor_listener.get_new()
            assert type(vendors) == list

    def test_import_work_center(self, caplog):
        integration = Integration()
        wc_importer = AcumaticaWorkCenterImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            wc_importer.run("0BCU")
            assert "Processing work center 0BCU" in caplog.text
            assert url_is_in_request_history(f"entity/Manufacturing/{MANUFACTURING_VERSION}/WorkCenter", "GET", m)

    def test_get_new_wc(self, caplog):
        integration = Integration()
        AcumaticaClient(base_url="https://testapi.com")
        wc_listener = importer.AcumaticaWorkCenterImportListener(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_alts(m)
            wcs = wc_listener.get_new()
            assert type(wcs) == list

    def test_outside_service(self, caplog):
        integration = Integration()
        service_importer = AcumaticaOutsideServiceImporter(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            service_importer.run("BLAST-OTHER")
            assert "Processing Non Stock Item BLAST-OTHER" in caplog.text
            assert url_is_in_request_history(f"entity/Default/{DEFAULT_VERSION}/NonStockItem", "GET", m)

    def test_get_new_osv(self, caplog):
        integration = Integration()
        AcumaticaClient(base_url="https://testapi.com")
        osv_listener = importer.AcumaticaOutsideServiceImportListener(integration)
        with requests_mock.Mocker(real_http=True) as m:
            register_alts(m)
            osvs = osv_listener.get_new()
            assert type(osvs) == list

    def test_create_pc_column(self, caplog):
        proc = AcumaticaPurchasedComponentImportProcessor(AcumaticaPurchasedComponentImporter)
        proc.create_custom_purchased_component_column("test", "invalid")
        assert "Could not create custom Purchased Component Column" in caplog.text

    def test_create_new_pc(self, caplog):
        proc = AcumaticaPurchasedComponentImportProcessor(AcumaticaPurchasedComponentImporter)
        AcumaticaClient(base_url="https://testapi.com")
        PaperlessClient(access_token='null')
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            purchased_component = StockItem.get_first({'InventoryID': 'AKM1-420-260'})
            proc._create_new_paperless_component(purchased_component)
            assert "Failed to create purchased component" in caplog.text


if __name__ == '__main__':
    unittest.main()

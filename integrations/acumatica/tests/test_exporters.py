from unittest import TestCase
import os
import json
import re
import requests_mock
from acumatica.api_models.acumatica_models import Customer, Contact, BaseObject
from acumatica.client import AcumaticaClient
from acumatica.utils import StockItemData
from acumatica.exporter.exporter import AcumaticaOrderExporter
from baseintegration.integration import Integration
from acumatica.api_models.acumatica_models import DEFAULT_VERSION


def loadfile(filename: str):
    with open(os.path.join(os.path.dirname(__file__), f"data/{filename}"), 'r') as f:
        return json.load(f)


def register_mocks(mocker):
    account_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/Customer")
    token_matcher = re.compile("identity/connect/token")
    contact_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/Contact")
    customer_matcher = re.compile(f"entity/Default/{DEFAULT_VERSION}/Customer")
    contact_empty = re.compile(f"entity/Default/{DEFAULT_VERSION}/Contact")

    mocker.put(account_matcher, json=loadfile('accounts.json'), status_code=200)
    mocker.post(token_matcher, json={"access_token": "abc", "refresh_token": "abc", "expires_in": 3600},
                status_code=200)
    mocker.put(contact_matcher, json=loadfile('get_contacts.json'), status_code=200)
    mocker.get(customer_matcher, json=loadfile('accounts.json'), status_code=200)
    mocker.get(contact_empty, json=[], status_code=200)


class TestOrderDetail(TestCase):

    def test_create_detail(self):
        mock_order = loadfile('put_sale_order_detail.json')
        self.assertIn('id', mock_order)

    def test_create_account(self):
        AcumaticaClient(base_url="https://testapi.com")
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            create = Customer.create(data={}, skip_keys=True, skip_serializer=True)
            assert type(create) == list

    def test_update_account(self):
        AcumaticaClient(base_url="https://testapi.com")
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            mod = Contact.update_resource(data={})
            assert type(mod) == Contact

    def test_get_first(self):
        AcumaticaClient(base_url="https://testapi.com")
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            first = Customer.get_first(filters={})
            assert type(first) == Customer

    def test_get_empty(self):
        AcumaticaClient(base_url="https://testapi.com")
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            with self.assertRaises(Exception):
                Contact.get_first(filters={})

    def test_init(self):
        sidata = StockItemData(component={}, order_item={}, is_root_item=True, is_make_part=True, is_purchased=False)
        assert type(sidata) == StockItemData

    def test_add_values(self):
        go = BaseObject.add_value_keys({'id': 'novalueadd', 'some': 'data'})
        assert 'value' in go.get('some').keys()

    def test_exporter(self):
        integration = Integration()
        exporter = AcumaticaOrderExporter(integration)
        exporter._setup_erp_client()
        assert type(exporter.client) == AcumaticaClient

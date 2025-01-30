import json
import pytest
import os

from dynamics.client_factory import ClientFactory
from dynamics.objects.customer import Customer
from dynamics.tests.utils import DynamicsMock, with_mocks


@pytest.fixture
def setup_integration():
    with open(os.path.join(os.path.dirname(__file__), "data/customers.json"), 'r') as f:
        mock_list_data = f.read()
    with open(os.path.join(os.path.dirname(__file__), "data/single_customer.json"), 'r') as f:
        mock_single_data = f.read()
    client = ClientFactory.build_client_from_config(secrets=None, test_mode=True)
    return client, mock_list_data, mock_single_data


class TestBaseObject:
    def test_get_all(self, setup_integration):
        client, mock_list_data, mock_single_data = setup_integration
        filters = {
            'teststr': 'str',
            'testnum': 1
        }
        expected_params = {
            '$filter': "teststr eq 'str' and testnum eq 1"
        }

        def run_test(call_data, get_args):
            Customer.get_all(filters)
            assert call_data[client, 'get_resource'].call_args_list[0][1]['params'] == expected_params

        with_mocks(run_test, [
            DynamicsMock(client, 'get_resource', return_val=json.loads(mock_list_data))
        ])

    def test_update(self, setup_integration):
        client, mock_list_data, mock_single_data = setup_integration
        test_keys_1 = 'testid1'
        expected_url_1 = f"{Customer.resource_name}('testid1')"
        test_keys_2 = ['testid1', 'testid2']
        expected_url_2 = f"{Customer.resource_name}('testid1', 'testid2')"

        def run_test(call_data, get_args):
            Customer.update(test_keys_1)
            Customer.update(test_keys_2)
            assert call_data[client, 'get_resource'].call_args_list[0][0][0] == expected_url_1
            assert call_data[client, 'get_resource'].call_args_list[1][0][0] == expected_url_2

        with_mocks(run_test, [
            DynamicsMock(client, 'get_resource', return_val=json.loads(mock_single_data)),
            DynamicsMock(client, 'patch_resource', return_val=json.loads(mock_single_data))
        ])

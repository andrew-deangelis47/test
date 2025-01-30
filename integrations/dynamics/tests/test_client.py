import json
import pytest
import time
from unittest.mock import ANY
from types import SimpleNamespace
import os
from unittest import mock

from dynamics.client_factory import ClientFactory
from dynamics.exceptions import DynamicsException, DynamicsNotFoundException


def mock_request(method, url, response):
    def mock_fn(*args, **kwargs):
        if kwargs["url"] == url:
            return response
        else:
            raise Exception('Endpoint not mocked:', kwargs["url"])

    return mock.patch(f'requests.{method}', side_effect=mock_fn)


@pytest.fixture
def setup_integration():
    with open(os.path.join(os.path.dirname(__file__), "data/customers.json"), 'r') as f:
        mock_data = f.read()
    client = ClientFactory.build_client_from_config(secrets=None, test_mode=True)

    def mock_authentication():
        return mock_request('post', client.token_url, SimpleNamespace(
            status_code=200,
            json=lambda: {
                "access_token": "test_token",
            }
        ))

    def mock_good_response():
        return mock_request('request', f'{client.odata_base_url}Customer_Card', SimpleNamespace(
            status_code=200,
            json=lambda: json.loads(mock_data)
        ))

    return client, mock_data, mock_authentication, mock_good_response


class TestClient:
    def test_token_error(self, setup_integration):
        client, mock_data, mock_authentication, mock_good_response = setup_integration
        with mock_request('post', client.token_url, SimpleNamespace(
                status_code=400,
                json=lambda: {
                    "code": "BAD_REQUEST",
                }
        )):
            with pytest.raises(DynamicsException):
                client.get_resource('Customer_Card')

    def test_renew_expired_token(self, setup_integration):
        client, mock_data, mock_authentication, mock_good_response = setup_integration
        client.access_token = {
            "access_token": "some_token",
            "expires_on": time.time() - 1
        }
        with mock_authentication() as auth_mock:
            with mock_good_response():
                client.get_resource('Customer_Card')
                assert auth_mock.called

    def test_no_renew_valid_token(self, setup_integration):
        client, mock_data, mock_authentication, mock_good_response = setup_integration
        client.access_token = {
            "access_token": "some_token",
            "expires_on": time.time() + client.TOKEN_EXPIRATION_TOLERANCE + 1
        }
        with mock_authentication() as auth_mock:
            with mock_good_response():
                client.get_resource('Customer_Card')
                assert not auth_mock.called

    def test_get_resource_ok(self, setup_integration):
        client, mock_data, mock_authentication, mock_good_response = setup_integration
        with mock_authentication():
            with mock_good_response():
                retval = client.get_resource('Customer_Card')
                assert retval == json.loads(mock_data)

    def test_get_resource_error(self, setup_integration):
        client, mock_data, mock_authentication, mock_good_response = setup_integration
        with mock_authentication():
            with mock_request('request', f'{client.odata_base_url}Customer_Card', SimpleNamespace(
                    status_code=400,
                    json=lambda: {}
            )):
                with pytest.raises(DynamicsException):
                    client.get_resource('Customer_Card')

    def test_get_resource_not_found_error(self, setup_integration):
        client, mock_data, mock_authentication, mock_good_response = setup_integration
        with mock_authentication():
            with mock_request('request', f'{client.odata_base_url}Customer_Card', SimpleNamespace(
                    status_code=404,
                    json=lambda: {
                        'error': {
                            'code': 'BadRequest_ResourceNotFound'
                        }
                    }
            )):
                with pytest.raises(DynamicsNotFoundException):
                    client.get_resource('Customer_Card')

    def test_post_resource_ok(self, setup_integration):
        client, mock_data, mock_authentication, mock_good_response = setup_integration
        with mock_authentication():
            with mock_good_response() as response_mock_data:
                retval = client.post_resource('Customer_Card', json.loads(mock_data))
                assert retval == json.loads(mock_data)
                response_mock_data.assert_called_once_with(
                    url=f'{client.odata_base_url}Customer_Card',
                    method='POST',
                    json=json.loads(mock_data),
                    headers=ANY,
                    params=ANY
                )

import json
import requests
import pytest
from unittest.mock import patch
from plex_v2.client import PlexClient
from plex_v2.exceptions import (
    PlexException,
    PlexMalformedRequestException,
    PlexRequestNotAuthenticatedException,
    PlexRequestProcessingErrorException,
    PlexResourceNotFoundException,
    PlexValidationFailureException,
)
from types import SimpleNamespace
import os


class TestClient:
    def setup_method(self):
        self.mock_api_key = 'mock_api_key'
        self.mock_base_url = 'mock_base_url'
        with open(os.path.join(os.path.dirname(__file__), "data/part.json"), 'r') as f:
            self.mock_part_text = f.read()
        self.client = PlexClient(api_key=self.mock_api_key, base_url=self.mock_base_url)
        self.headers = {
            'Accept': 'application/json',
            'X-Plex-Connect-Api-Key': self.mock_api_key,
            'Content-Type': 'application/json'
        }

    def test_request_not_authenticated(self):
        with patch.object(requests, 'get', return_value=SimpleNamespace(
                status_code=401,
                content='',
                json=lambda: {
                    "code": "REQUEST_NOT_AUTHENTICATED",
                }
        )):
            id_ = 1
            with pytest.raises(PlexRequestNotAuthenticatedException):
                self.client.get_resource('parts', id_)

    def test_resource_not_found(self):
        with patch.object(requests, 'get', return_value=SimpleNamespace(
                status_code=404,
                content='',
                json=lambda: {
                    "code": "RESOURCE_NOT_FOUND",
                }
        )):
            id_ = 1
            with pytest.raises(PlexResourceNotFoundException):
                self.client.get_resource('parts', id_)

    def test_request_processing_error(self):
        with patch.object(requests, 'get', return_value=SimpleNamespace(
                status_code=500,
                content='',
                json=lambda: {
                    "code": "ERROR",
                }
        )):
            id_ = 1
            with pytest.raises(PlexRequestProcessingErrorException):
                self.client.get_resource('parts', id_)

    def test_other_response_status_code(self):
        with patch.object(requests, 'get', return_value=SimpleNamespace(
                status_code=502,
                content='Bad Gateway',
        )):
            id_ = 1
            with pytest.raises(PlexException):
                self.client.get_resource('parts', id_)

    def test_get_resource_no_api_key(self):
        client_no_api_key = PlexClient()
        with pytest.raises(PlexValidationFailureException):
            id_ = 1
            client_no_api_key.get_resource('parts', id_)

    def test_get_resource_ok(self):
        with patch.object(requests, 'get', return_value=SimpleNamespace(
                status_code=200,
                json=lambda: json.loads(self.mock_part_text)
        )):
            id_ = 1
            retval = self.client.get_resource('parts', id_)
            assert retval == json.loads(self.mock_part_text)

    def test_get_resource_does_not_exist(self):
        with patch.object(requests, 'get', return_value=SimpleNamespace(
                status_code=400,
                content='',
                json=lambda: {
                    "code": "REQUEST_VALIDATION_FAILED",
                }
        )):
            with pytest.raises(PlexValidationFailureException):
                id_ = 1
                self.client.get_resource('parts', id_)

    def test_get_resource_malformed_request(self):
        with patch.object(requests, 'get', return_value=SimpleNamespace(
                status_code=400,
                content='',
                json=lambda: {
                    "code": "REQUEST_MALFORMED",
                }
        )):
            with pytest.raises(PlexMalformedRequestException):
                id_ = 1
                self.client.get_resource('parts', id_)

    def test_get_resource_other_error(self):
        with patch.object(requests, 'get', return_value=SimpleNamespace(
                status_code=400,
                content='',
                json=lambda: {
                    "code": "OTHER_ERROR",
                }
        )):
            with pytest.raises(PlexException):
                id_ = 1
                self.client.get_resource('parts', id_)

    def test_create_resource_ok(self):
        with patch.object(requests, 'post', return_value=SimpleNamespace(
                status_code=200,
                json=lambda: json.loads(self.mock_part_text),
        )) as post:
            self.client.create_resource('parts', json.loads(self.mock_part_text))
            post.assert_called_once_with(
                f'{self.mock_base_url}/parts',
                headers=self.headers,
                data=json.loads(self.mock_part_text),
                params=None,
                json=None,
                auth=None
            )

    def test_create_resource_failure(self):
        with patch.object(requests, 'post', return_value=SimpleNamespace(
                status_code=400,
                content='',
                json=lambda: {
                    "code": "REQUEST_VALIDATION_FAILED",
                }
        )):
            with pytest.raises(PlexValidationFailureException):
                self.client.create_resource('parts', json.loads(self.mock_part_text))

    def test_create_resource_malformed_request(self):
        with patch.object(requests, 'post', return_value=SimpleNamespace(
                status_code=400,
                content='',
                json=lambda: {
                    "code": "REQUEST_MALFORMED",
                }
        )):
            with pytest.raises(PlexMalformedRequestException):
                self.client.create_resource('parts', json.loads(self.mock_part_text))

    def test_get_resource_list(self):
        pass

    def test_delete_resource(self):
        pass

import json
import time
from types import SimpleNamespace
from datetime import datetime
import os

import requests
from requests.auth import HTTPBasicAuth

from baseintegration.datamigration import logger

from acumatica.exceptions import AcumaticaException, AcumaticaValidationFailureException, \
    AcumaticaMalformedRequestException, AcumaticaRequestNotAuthenticatedException, \
    AcumaticaRequestProcessingErrorException, AcumaticaResourceNotFoundException

from configparser import RawConfigParser


class AcumaticaClient:
    """
    This class is used to make all calls to the Acumatica API.
    """
    _instance = None
    _token_lifespan = 3600  # 1 hr in secs

    def __new__(cls, **kwargs):
        """
        Create or return the AcumaticaClient Singleton.
        """
        if AcumaticaClient._instance is None:
            AcumaticaClient._instance = object.__new__(cls)
        instance = AcumaticaClient._instance

        # If nothing provided, connects to test environment. Maybe it should be prod?
        instance.base_url = kwargs.get('base_url', os.getenv('BASE_URL'))
        instance.username = kwargs.get('username', os.getenv('USERNAME'))
        instance.password = kwargs.get('password', os.getenv('PASSWORD'))
        instance.client_secret = kwargs.get('client_secret', os.getenv('CLIENT_SECRET'))
        instance.client_id = kwargs.get('client_id', os.getenv('CLIENT_ID'))

        instance.last_token_date = datetime(2022, 1, 1, 0, 0, 0)
        instance.token = None

        cls._instance = instance
        return instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    __instance = None

    METHODS = SimpleNamespace(
        DELETE='delete', GET='get', PATCH='patch', POST='post', PUT='put'
    )

    @classmethod
    def get_token(cls):
        parser = RawConfigParser()
        parser.read(os.path.join(os.path.dirname(__file__), "../../secrets.ini"))
        parser_dict = parser._sections

        expires_at = parser_dict['Paperless'].get('acumatica_expires_at')
        if not expires_at:
            # Token not set yet, get a new one
            cls._generate_new_token()
        elif time.time() < float(expires_at):
            # Use the existing valid token
            cls._instance.token = parser_dict['Paperless'].get('acumatica_access_token')
        else:
            # Token has expired, get a new one using the refresh token
            cls.refresh_token(parser_dict['Paperless'].get('acumatica_refresh_token'))
        return cls._instance.token

    @classmethod
    def _generate_new_token(cls):
        token_endpoint = f'{cls._instance.base_url}identity/connect/token'
        data = {'grant_type': 'password',
                'client_id': cls._instance.client_id,
                'client_secret': cls._instance.client_secret,
                'username': cls._instance.username,
                'password': cls._instance.password,
                'scope': 'api offline_access'
                }
        resp = requests.post(url=token_endpoint, data=data)
        access_token = resp.json().get('access_token', None)
        if access_token:
            cls.save_token_response(resp=resp.json())
            cls._instance.token = access_token

    @classmethod
    def refresh_token(cls, refresh_token):
        token_endpoint = f'{cls._instance.base_url}identity/connect/token'
        data = {'grant_type': 'refresh_token',
                'client_id': cls._instance.client_id,
                'client_secret': cls._instance.client_secret,
                'refresh_token': refresh_token
                }
        resp = requests.post(url=token_endpoint, data=data)
        access_token = resp.json().get('access_token', None)
        if access_token:
            cls.save_token_response(resp=resp.json())
            cls._instance.token = access_token

    @classmethod
    def save_token_response(cls, resp: object):
        parser = RawConfigParser()
        parser.read(os.path.join(os.path.dirname(__file__), "../../secrets.ini"))
        parser.set("Paperless", "acumatica_access_token", resp['access_token'])
        parser.set("Paperless", "acumatica_refresh_token", resp['refresh_token'])
        parser.set("Paperless", "acumatica_expires_at", resp['expires_in'] + time.time())
        config = open(os.path.join(os.path.dirname(__file__), "../../secrets.ini"), "w")
        parser.write(config, space_around_delimiters=False)
        config.close()

    def get_authenticated_headers(self) -> dict:
        """
        Get the headers including authorization
        return: dict of headers including authorization
        """

        auth_header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_token()}'
        }
        return auth_header

    def request(self, url=None, method=None, data=None, params=None, json=None, datasource: bool = False):  # noqa: C901
        req_url = f'{self.base_url}/{url}'
        headers = self.get_authenticated_headers()
        auth = None

        if datasource:
            req_url = f'{self.base_url_data_source}/{url}'
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
            auth = HTTPBasicAuth(self.username, self.password)

        # logger.info(f'{req_url} \n {params} \n {data} \n {headers}')
        method_to_call = getattr(requests, method)
        if data is not None:
            resp = method_to_call(req_url, headers=headers, data=data, params=params, json=json, auth=auth)
        else:
            resp = method_to_call(req_url, headers=headers, params=params, auth=auth)

        if (
                resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204
        ):
            return resp
        elif resp.status_code == 400:
            # There are 3 possible 400 exceptions based on the 'code' received
            code = None
            try:
                data = resp.json()
                code = data.get('code', None)
            except:
                # Just in case there is a bad payload, we want to at least provide a generic error
                pass

            if code == 'REQUEST_VALIDATION_FAILED':
                raise AcumaticaValidationFailureException(
                    message=f"Acumatica Validation Request Failed: {resp.content}",
                    error_code=resp.status_code,
                )

            elif code == 'REQUEST_MALFORMED':
                raise AcumaticaMalformedRequestException(
                    message=f"Acumatica Malformed Request: {resp.content}",
                    error_code=resp.status_code,
                )
            else:
                raise AcumaticaException(
                    message=f"Failed to update resource: {resp.content}",
                    error_code=resp.status_code,
                )
        elif resp.status_code == 401:
            logger.info('got 401')
            try:
                data = resp.json()
                code = data.get('code', None)
                logger.info(f'Response code {code}')
            except Exception:
                # Just in case there is a bad payload, we want to at least provide a generic error
                raise AcumaticaRequestNotAuthenticatedException(
                    message=f"Not authorized to access url: {req_url}"
                )

        elif resp.status_code == 404:
            raise AcumaticaResourceNotFoundException(
                message=f"Acumatica resource not found: {url}"
            )
        elif resp.status_code == 500:
            raise AcumaticaRequestProcessingErrorException(
                message=f"Acumatica Error processing request: {url}, message: {resp.content}"
            )
        else:

            try:
                resp_json = resp.json()
                if resp_json.get('message') is None:
                    message = resp_json
                    logger.error(f'Error -> {message}')
                else:
                    message = resp_json['message']
            # raise generic error if there is no error message
            except Exception:
                raise AcumaticaException(
                    message="Request failed with status code {}".format(resp.status_code),
                )
            raise AcumaticaException(message=message, error_code=resp.status_code)

    def get_resource_list(self, list_url: str, params=None):
        resp = self.request(url=list_url, method=self.METHODS.GET, params=params)
        return resp.json()

    def get_resource(self, resource_url: str, identifier, params=None):
        """
            takes a resource type
            performs GET request for last updated + 1
            will return true if the next object exists, else false
        """
        url = "{}/{}".format(resource_url, identifier) if identifier else "{}".format(resource_url)
        resp = self.request(url=url, method=self.METHODS.GET, params=params)
        return resp.json()

    def create_resource(self, resource_url, data):

        payload = json.dumps(data)
        resp = self.request(url=resource_url, method=self.METHODS.POST, data=payload)
        if resp.status_code != 204:
            return resp.json()
        return resp

    def update_resource(self, resource_url, id, data):
        """
            takes a resource type
            performs GET request for last updated + 1
            will return true if the next object exists, else false
        """

        req_url = '{}/{}'.format(resource_url, id) if id else resource_url
        resp = self.request(url=req_url, method=self.METHODS.PUT, data=data)
        if resp.status_code != 200:
            logger.info(resp.text)
        return resp.json()

    def delete_resource(self, resource_url, id):
        """
        """
        self.get_authenticated_headers()

        req_url = '{}/{}'.format(resource_url, id)

        self.request(url=req_url, method=self.METHODS.DELETE)
        return

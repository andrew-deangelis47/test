import time
from types import SimpleNamespace

import requests
from requests.auth import HTTPBasicAuth

from plex.exceptions import PlexException, PlexValidationFailureException, PlexResourceNotFoundException, \
    PlexMalformedRequestException, PlexRequestNotAuthenticatedException, PlexRequestProcessingErrorException

from baseintegration.datamigration import logger


class PlexClient:
    """
    This class is used to make all calls to the plex API.
    """
    _instance = None

    def __new__(cls, **kwargs):
        """
        Create or return the PlexClient Singleton.
        """
        if PlexClient._instance is None:
            PlexClient._instance = object.__new__(cls)
        instance = PlexClient._instance

        instance.api_key = kwargs.get('api_key', None)
        # If nothing provided, connects to test environment. Maybe it should be prod?
        instance.base_url = kwargs.get('base_url', 'https://test.connect.plex.com/mdm/v1/')
        instance.base_url_data_source = kwargs.get('base_url_data_source', 'https://test.cloud.plex.com/api/')
        instance.username = kwargs.get('username', None)
        instance.password = kwargs.get('password', None)
        instance.pcn = kwargs.get('pcn', None)
        cls._instance = instance
        return instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    __instance = None

    METHODS = SimpleNamespace(
        DELETE='delete', GET='get', PATCH='patch', POST='post', PUT='put'
    )

    def get_authenticated_headers(self) -> dict:
        """
        Get the headers including authorization
        return: dict of headers including authorization
        """
        if not self.api_key:
            raise PlexValidationFailureException(
                message='Unable to authenticate call',
                detail='You are trying to perform an HTTP request without an Plex API Key.',
            )
        auth_header = {
            'Accept': 'application/json',
            'X-Plex-Connect-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        if self.pcn:
            auth_header['X-Plex-Connect-Customer-Id'] = self.pcn
        return auth_header

    def request(self, url=None, method=None, data=None, params=None, json=None, datasource: bool = False):  # noqa: C901
        req_url = f'{self.base_url}/{url}'
        headers = self.get_authenticated_headers()
        auth = None
        if datasource:
            req_url = f'{self.base_url_data_source}/{url}'
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
            auth = HTTPBasicAuth(self.username, self.password)

        method_to_call = getattr(requests, method)
        if data is not None:
            resp = method_to_call(req_url, headers=headers, data=data, params=params, json=json, auth=auth)
        else:
            resp = method_to_call(req_url, headers=headers, params=params, auth=auth)

        if (
                resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204
        ):
            return resp
        elif resp.status_code == 429:
            try:
                # FIXME: Have not tested, and there may not be a throttling on the Plex API. Here for future usage,
                #  but almost certainly needs updating
                message = resp.json().get('message')
                logger.info(message)
                wait_time = int(message[message.find('in') + 3: message.find('second') - 1]) + 1
                time.sleep(wait_time)
            except (
                    TypeError,
                    AttributeError,
                    ValueError,
            ) as e:  # catch any exception while trying to access the backoff message
                logger.error(e)
                time.sleep(60)
            finally:
                return self.request(url=url, method=method, data=data, params=params, auth=auth)
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
                raise PlexValidationFailureException(
                    message=f"Plex Validation Request Failed: {resp.content}",
                    error_code=resp.status_code,
                )

            elif code == 'REQUEST_MALFORMED':
                raise PlexMalformedRequestException(
                    message=f"Plex Malformed Request: {resp.content}",
                    error_code=resp.status_code,
                )
            else:
                raise PlexException(
                    message=f"Failed to update resource: {resp.content}",
                    error_code=resp.status_code,
                )
        elif resp.status_code == 401 and resp.json()['code'] == 'REQUEST_NOT_AUTHENTICATED':
            raise PlexRequestNotAuthenticatedException(
                message=f"Not authorized to access url: {req_url}"
            )
        elif resp.status_code == 404:
            raise PlexResourceNotFoundException(
                message=f"Plex resource not found: {url}"
            )
        elif resp.status_code == 500:
            raise PlexRequestProcessingErrorException(
                message=f"Plex Error processing request: {url}, message: {resp.content}"
            )
        else:
            try:
                resp_json = resp.json()
                message = resp_json['message']
            # raise generic error if there is no error message
            except Exception:
                raise PlexException(
                    message="Request failed with status code {}".format(resp.status_code),
                )
            raise PlexException(message=message, error_code=resp.status_code)

    def get_resource_list(self, list_url: str, params=None):
        resp = self.request(url=list_url, method=self.METHODS.GET, params=params)
        return resp.json()

    def get_resource(self, resource_url: str, identifier, params=None):
        """
            takes a resource type
            performs GET request for last updated + 1
            will return true if the next object exists, else false
        """
        url = "{}/{}".format(resource_url, identifier)
        resp = self.request(url=url, method=self.METHODS.GET, params=params)
        return resp.json()

    def create_resource(self, resource_url, data):
        """
        """
        resp = self.request(url=resource_url, method=self.METHODS.POST, data=data)
        return resp.json()

    def update_resource(self, resource_url, id, data):
        """
            takes a resource type
            performs GET request for last updated + 1
            will return true if the next object exists, else false
        """

        req_url = '{}/{}'.format(resource_url, id)

        resp = self.request(url=req_url, method=self.METHODS.PUT, data=data)
        return resp.json()

    def delete_resource(self, resource_url, id):
        """
        """
        self.get_authenticated_headers()

        req_url = '{}/{}'.format(resource_url, id)

        self.request(url=req_url, method=self.METHODS.DELETE)
        return

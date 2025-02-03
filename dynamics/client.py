import time
import requests

from dynamics.exceptions import DynamicsException, DynamicsNotFoundException


class DynamicsClient(object):

    # number of seconds before expiration to trigger a renewal
    TOKEN_EXPIRATION_TOLERANCE = 60

    _instance = None
    sent = False

    def __new__(cls, **kwargs):
        """
        Create or return the DynamicsClient Singleton.
        """
        if DynamicsClient._instance is None:
            DynamicsClient._instance = object.__new__(cls)
        instance = DynamicsClient._instance

        instance.tenant_id = kwargs.get('tenant_id')
        instance.client_secret = kwargs.get('client_secret')
        instance.environment_name = kwargs.get('environment_name')
        instance.client_id = kwargs.get('client_id')
        instance.company_name = kwargs.get('company_name')

        # application ID of Business Central
        instance.bc_app_id = '996def3d-b36c-4153-8607-a6fd3c01b89f'
        instance.token_url = f'https://login.microsoftonline.com/{instance.tenant_id}/oauth2/token'
        instance.base_url = f'https://api.businesscentral.dynamics.com/v2.0/{instance.environment_name}/'
        instance.odata_base_url = \
            f'{instance.base_url}OData/Company({DynamicsClient.format_query_key(instance.company_name)})/'

        instance.access_token = None
        instance.token_expiration = None

        return instance

    @staticmethod
    def format_query_key(key) -> str:
        """
        Formats a query key to be used in OData filters.
        """
        if isinstance(key, str):
            key_quotes_escaped = "''".join(key.split("'"))  # double each single quote
            return f"'{key_quotes_escaped}'"
        else:
            return key

    @classmethod
    def get_instance(cls):
        return cls._instance

    def get_access_token(self):
        headers = {
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        }
        form_data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'resource': self.bc_app_id,
            'grant_type': 'client_credentials'
        }
        resp = requests.post(url=self.token_url, headers=headers, data=form_data)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise DynamicsException(
                message=f"Failed to get resource from url: {self.token_url} - {resp.json()}",
                error_code=resp.status_code
            )

    def access_token_expired(self):
        return time.time() > int(self.access_token['expires_on']) - self.TOKEN_EXPIRATION_TOLERANCE

    def get_authenticated_headers(self):
        if not self.access_token or self.access_token_expired():
            self.get_instance().access_token = self.get_access_token()

        return {
            'Accept': 'application/json',
            'Authorization': "Bearer %s" % self.access_token['access_token'],
            'Connection': 'keep-alive'
        }

    def request(self, method: str, url: str, data: dict = {}, params={}, extra_headers={}):
        headers = {
            **self.get_authenticated_headers(),
            **extra_headers
        }
        base_url = self.odata_base_url
        req_url = f"{base_url}{url}"
        filtered_data = {k: v for (k, v) in data.items() if v is not None}  # filter out None values in body

        resp = requests.request(
            url=req_url,
            method=method,
            headers=headers,
            json=filtered_data,
            params=params
        )

        if resp.status_code in [200, 201, 204]:
            return resp.json()
        else:
            message = f"Failed to {method} resource: {req_url} with {filtered_data} - {resp.json()}"
            error_code = resp.json() and resp.json().get('error') and resp.json().get('error').get('code')
            if resp.status_code in [404] and error_code == 'BadRequest_ResourceNotFound':
                raise DynamicsNotFoundException(message=message)
            else:
                raise DynamicsException(
                    message=message,
                    error_code=resp.status_code
                )

    def get_resource(self, url: str, params={}) -> dict:
        body = self.request('GET', url, params=params)
        return body

    def patch_resource(self, url: str, data: dict, params={}, headers={}) -> dict:
        body = self.request('PATCH', url, data, params=params, extra_headers=headers)
        return body

    def delete_resource(self, url: str, params={}) -> dict:
        body = self.request('DELETE', url, params=params)
        return body

    def post_resource(self, url: str, data: dict, params={}) -> dict:
        body = self.request('POST', url, data, params=params)
        return body

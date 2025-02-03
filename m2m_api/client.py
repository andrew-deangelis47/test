import requests
from requests import Response
from types import SimpleNamespace
import time

from m2m_api.exceptions import M2MException
from baseintegration.exporter import logger

from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class M2MClient(object):

    _instance = None

    METHODS = SimpleNamespace(
        DELETE='delete', GET='get', PATCH='patch', POST='post', PUT='put'
    )

    def __new__(cls, **kwargs):
        """
        Create or return the M2MClient Singleton.
        """
        if M2MClient._instance is None:
            M2MClient._instance = object.__new__(cls)
        instance = M2MClient._instance

        instance.base_url = kwargs.get('base_url', None)
        instance.client_secret = kwargs.get('client_secret')
        instance.client_id = kwargs.get('client_id')
        instance.token_url = kwargs.get('token_url')
        instance.token_scope = kwargs.get('token_scope')
        instance.company_id = kwargs.get('company_id')
        instance.access_token = None

        # By default we will not verify the certificate on the SSL handshake
        instance.verify_ssl_cert = kwargs.get('verify_ssl_cert', False)

        return instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    def get_authenticated_headers(self):
        if self.access_token_expired():
            self.get_instance().access_token = self.get_access_token()

        return {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token["access_token"]}',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'CompanyID': f'{self.company_id}'
        }

    def get_access_token(self):
        payload = f"grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}@&scope={self.token_scope}"
        headers = {
            'CompanyID': f'{self.company_id}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        resp: Response = requests.request("POST", self.token_url, headers=headers, data=payload)

        token_get_time = time.time()
        access_token_dict = resp.json()
        access_token_dict['expires_on'] = token_get_time + access_token_dict['expires_in']
        return access_token_dict

    def access_token_expired(self):
        # get the token if it's the first time
        if self.access_token is None:
            return True

        return time.time() > int(self.access_token['expires_on'])

    def get_resource_list(self, list_url: str, params=None):
        resp = self.request(url=list_url, method=self.METHODS.GET, params=params)
        json_response = resp.json()
        if 'value' in json_response:
            return resp.json()['value']
        return json_response

    def request(self, url=None, method=None, data=None, params=None, json_payload=None):  # noqa: C901
        req_url = f'{self.base_url}/{url}'
        if json_payload is not None:
            logger.info(json_payload)
        logger.info("\n\n")
        headers = self.get_authenticated_headers()
        auth = None

        method_to_call = getattr(requests, method)
        if data is not None:
            logger.info(data)

        if data is not None:
            resp = method_to_call(req_url, headers=headers, data=data, params=params, json=json_payload, auth=auth)
        else:
            resp = method_to_call(req_url, headers=headers, params=params, auth=auth)

        if (
                resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204
        ):
            return resp
        else:
            try:
                resp_json = resp.json()
                message = ''
                try:
                    message = resp_json['message']
                except KeyError:
                    pass
            # raise generic error if there is no error message
            except Exception:
                raise M2MException(
                    message="Request failed with status code {}".format(resp.status_code),
                )
            raise M2MException(message=message, error_code=resp.status_code)

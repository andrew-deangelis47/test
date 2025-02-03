import simplejson as json
import requests
import base64

from epicor.exceptions import EpicorAuthorizationException, EpicorException, EpicorNotFoundException
from baseintegration.exporter import logger

from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class EpicorClient(object):
    VERSION_0 = 'v0.0'
    VALID_VERSIONS = [VERSION_0]

    _instance = None
    version = VERSION_0

    def __new__(cls, **kwargs):
        """
        Create or return the EpicorClient Singleton.
        """
        if EpicorClient._instance is None:
            EpicorClient._instance = object.__new__(cls)
        instance = EpicorClient._instance

        instance.base_url = kwargs.get('base_url', None)
        instance.password = kwargs.get('password', None)
        instance.username = kwargs.get('username', None)
        instance.api_key = kwargs.get('api_key', None)
        instance.company_name = kwargs.get('company_name', None)
        instance.bearer_token = kwargs.get('bearer_token', None)
        # TODO: ADD VERSION VALIDATION
        instance.version = kwargs.get('version', None)
        # By default we will not verify the certificate on the SSL handshake
        instance.verify_ssl_cert = kwargs.get('verify_ssl_cert', False)
        instance.plant_code = kwargs.get('plant_code', None)
        return instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    def get_authenticated_headers(self):
        if not self.api_key or not self.password or not self.username:
            raise EpicorAuthorizationException(
                message='Unable to authenticate call',
                detail='You are trying to perform an HTTP request without a proper credentials.'
            )

        userpass = self.username + ':' + self.password
        encoded_u = base64.b64encode(userpass.encode()).decode()
        bearer_token = self.bearer_token  # noqa: F841
        company_name = self.company_name
        plant_code = self.plant_code
        if plant_code and company_name:
            return {
                'Accept': 'application/json',
                'Authorization': "Basic %s" % encoded_u,
                'x-api-key': self.api_key,
                'Content-Type': 'application/json',
                'User-Agent': 'python-epicorSDK {}'.format(self.version),
                'CallSettings': str({"Company": company_name, "Plant": plant_code})
            }
        else:
            return {
                'Accept': 'application/json',
                'Authorization': "Basic %s" % encoded_u,
                'x-api-key': self.api_key,
                'Content-Type': 'application/json',
                'User-Agent': 'python-epicorSDK {}'.format(self.version)
            }

    def get_resource(self, resource_url: str, params: dict = None) -> dict:
        """
        """
        headers = self.get_authenticated_headers()

        req_url = "{}/{}".format(self.base_url, resource_url)
        resp = requests.request(method='GET',
                                url=req_url,
                                headers=headers,
                                params=params,
                                verify=self.verify_ssl_cert)
        if resp.status_code in [201, 200, 204]:
            return json.loads(resp.text, use_decimal=True)
        elif resp.status_code == 404:
            raise EpicorNotFoundException(
                message="Unable to locate object from url: {}".format(req_url)
            )
        elif resp.status_code == 401:
            try:
                if resp.json()['code'] == 'authentication_failed':
                    raise EpicorAuthorizationException(
                        message="Not authorized to access url: {}".format(req_url)
                    )
            except ValueError:
                error_msg = resp.text
                logger.info("Request returned 401 code.")
                raise EpicorException(
                    message=f"Failed to get resource from url: {req_url} - {error_msg} - {params}",
                    error_code=resp.status_code
                )
        else:
            try:
                error_msg = resp.json()
            except Exception:
                error_msg = resp.text
            raise EpicorException(
                message=f"Failed to get resource from url: {req_url} - {error_msg} - {params}",
                error_code=resp.status_code
            )

    def patch_resource(self, url: str, data: dict):
        """
        @param url:
        @param data:
        @return:
        """

        logger.debug(f'PATCHing resource: {url}: {data}')
        headers = self.get_authenticated_headers()
        req_url = '{}/{}'.format(self.base_url, url)
        resp = requests.patch(
            req_url,
            headers=headers,
            json=data,
            verify=self.verify_ssl_cert
        )
        if resp.status_code == 201 or resp.status_code == 200 or resp.status_code == 204:
            # There may not be any response text here. if not, don't try to load it:
            if resp.text:
                result = json.loads(resp.text, use_decimal=True)
            else:
                result = None
            logger.debug(f'PATCH Result : {result}')
            return result
        else:
            logger.info(f'Error in updating object: {resp.status_code} {resp.text}')
            raise EpicorException(
                message=f"Failed to PATCH resource: {url} - {resp.text}",
                error_code=resp.status_code
            )

    def post_resource(self, url: str, data: dict):
        """
        @param url:
        @param data:
        @return:
        """

        logger.debug(f'POSTing resource: {url}: {data}')
        headers = self.get_authenticated_headers()
        req_url = '{}/{}'.format(self.base_url, url)
        resp = requests.post(
            req_url,
            headers=headers,
            json=data,
            verify=self.verify_ssl_cert
        )
        if resp.status_code == 201 or resp.status_code == 200:
            result = json.loads(resp.text, use_decimal=True)
            return result
        else:
            logger.info(f'Error in calling method: {resp.status_code} {resp.text}')
            raise EpicorException(
                message=f"Failed to POST resource: {url} - {resp.text}",
                error_code=resp.status_code
            )

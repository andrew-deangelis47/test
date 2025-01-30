import unittest
import os
import re
import json
import requests_mock

from acumatica.client import AcumaticaClient


def loadfile(filename: str):
    with open(os.path.join(os.path.dirname(__file__), f"data/{filename}"), 'r') as f:
        return json.load(f)


def register_mocks(mocker):
    token_matcher = re.compile("identity/connect/token")
    not_auth_matcher = re.compile("/POST401")
    bad_request_matcher = re.compile("/GET400")
    too_many_matcher = re.compile("/GET404")
    internal_matcher = re.compile("/GET500")
    teapot_matcher = re.compile("/GET418")

    # register mockers
    mocker.post(token_matcher, json={"access_token": "abc", "refresh_token": "abc", "expires_in": 3600}, status_code=200)
    mocker.post(not_auth_matcher, status_code=401)
    mocker.put(bad_request_matcher, json={"code": 'REQUEST_VALIDATION_FAILED'}, status_code=400)
    mocker.get(too_many_matcher, json={"message": "retrying in 3 seconds"}, status_code=404)
    mocker.get(internal_matcher, json={"data": "blah"}, status_code=500)
    mocker.get(teapot_matcher, json={"data": "blah"}, status_code=418)


class TestToken:

    def test_get_token(self, caplog):
        client = AcumaticaClient(base_url='https://acumatica.cameronmfg.com')
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            token = client.get_token()
            assert token == 'abc'

    def test_generate_token(self, caplog):
        client = AcumaticaClient(base_url='https://acumatica.cameronmfg.com')
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            client._generate_new_token()
            assert client.token == 'abc'

    def test_refresh_token(self, caplog):
        client = AcumaticaClient(base_url='https://acumatica.cameronmfg.com')
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            client.refresh_token('abc')
            assert client.token == 'abc'


class TestClient(unittest.TestCase):
    def test_not_authenticated(self):
        from acumatica.exceptions import AcumaticaRequestNotAuthenticatedException
        client = AcumaticaClient(base_url='https://testapi.com')
        with requests_mock.Mocker(real_http=False) as m:
            register_mocks(m)
            with self.assertRaises(AcumaticaRequestNotAuthenticatedException) as cm:
                client.create_resource(resource_url="/POST401", data={"data": "some data"})
                assert "Acumatica Request Not Authenticated Exception: " in str(cm.exception)

    def test_400_error(self):
        from acumatica.exceptions import AcumaticaValidationFailureException
        client = AcumaticaClient(base_url='https://testapi.com')
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            with self.assertRaises(AcumaticaValidationFailureException) as cm:
                client.update_resource('/GET400', id=1, data=None)
            assert "Acumatica Validation Failure Exception:" in str(cm.exception)

    def test_404_error(self):
        from acumatica.exceptions import AcumaticaResourceNotFoundException
        client = AcumaticaClient(base_url='https://testapi.com')
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            with self.assertRaises(AcumaticaResourceNotFoundException) as cm:
                client.get_resource_list("/GET404")
            assert "Acumatica Resource Not Found Exception:" in str(cm.exception)

    def test_500_error(self):
        from acumatica.exceptions import AcumaticaRequestProcessingErrorException
        client = AcumaticaClient(base_url='https://testapi.com')
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            with self.assertRaises(AcumaticaRequestProcessingErrorException) as cm:
                client.get_resource_list("/GET500")
            assert "Acumatica Request Processing Error Exception:" in str(cm.exception)

    def test_418_error(self):
        from acumatica.exceptions import AcumaticaException
        client = AcumaticaClient(base_url='https://testapi.com')
        with requests_mock.Mocker(real_http=True) as m:
            register_mocks(m)
            with self.assertRaises(AcumaticaException) as cm:
                client.get_resource_list("/GET418")
            assert "{'data': 'blah'}" in str(cm.exception)


if __name__ == '__main__':
    unittest.main()

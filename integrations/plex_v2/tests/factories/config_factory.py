import unittest
from unittest.mock import create_autospec
from baseintegration.integration import Integration
from plex_v2.configuration import ERPConfigFactory


class PartFactoryTest(unittest.TestCase):

    TEST_API_KEY = "test_api_key"
    TEST_BASE_URL = "https://test.connect.plex.com"
    TEST_DATASOURCE_URL = "test_base_url_data_source"
    TEST_USERNAME = "test_username"
    TEST_PW = "test_password"
    TEST_PCN = "test_pcn"

    TEST_ORER_TIER = 123
    TEST_INTERVAL = 4000
    TEST_ACCOUNT_REACTIVATION_ENABLED = True

    def setUp(self) -> None:
        self.integration = create_autospec(Integration)
        self.integration.config_yaml = {
            "Plex": {
                "order_tier": self.TEST_ORER_TIER
            },
            "Importers": {
                "accounts": {
                    "account_reactivation_enabled": self.TEST_ACCOUNT_REACTIVATION_ENABLED
                }
            }
        }
        self.integration.secrets = {
            "Plex": {
                "base_url": self.TEST_BASE_URL,
                "api_key": self.TEST_API_KEY,
                "base_url_data_source": self.TEST_DATASOURCE_URL,
                "username": self.TEST_USERNAME,
                "password": self.TEST_PW,
                "pcn": self.TEST_PCN
            }
        }

    def test_erp_config_factory_creates_config_object_from_yaml(self):
        plex_config, plex_client = ERPConfigFactory.create_config(self.integration)
        assert plex_config.order_tier == self.TEST_ORER_TIER

    def test_erp_config_factory_creates_import_config_from_import_config_yaml(self):
        plex_config, plex_client = ERPConfigFactory.create_importer_config(self.integration, "accounts")
        assert plex_config.account_reactivation_enabled

    def test_erp_config_factory_creates_client_object_from_yaml(self):
        plex_config, plex_client = ERPConfigFactory.create_config(self.integration)
        assert plex_client.api_key == self.TEST_API_KEY
        assert plex_client.base_url == self.TEST_BASE_URL
        assert plex_client.base_url_data_source == self.TEST_DATASOURCE_URL
        assert plex_client.username == self.TEST_USERNAME
        assert plex_client.password == self.TEST_PW
        assert plex_client.pcn == self.TEST_PCN

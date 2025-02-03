from globalshop.integration import GlobalShopIntegration


class GSIntegrationTestClass(GlobalShopIntegration):

    def get_config_yaml(self):
        self.config_yaml = {"GlobalShop": {}, "Paperless": {}}

    def _get_secrets(self) -> dict:
        secrets = super()._get_secrets()
        secrets["GlobalShop"] = {
            "database": "GLOBAL",
            "server_name": '1.2.3.4',
            "username": 'willy',
            "password": 'waffle'
        }
        return secrets

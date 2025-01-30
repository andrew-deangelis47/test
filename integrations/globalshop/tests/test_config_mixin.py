class TestConfigMixin:

    def test_config_mixin(self):
        from globalshop.integration.config_mixin import GlobalShopConfigMixin

        class FakeIntegration:
            pass

            def __init__(self):
                self.config_yaml = {"GlobalShop": {}}
                self.secrets = {"GlobalShop": {}}

        class FakeDataMigration():

            def __init__(self, integration):

                self._setup_erp_config()

        class CustomDataMigration(GlobalShopConfigMixin, FakeDataMigration):
            pass

        fi = FakeIntegration()

        config_mix = CustomDataMigration(fi)

        assert config_mix.erp_name == 'GlobalShop'

        erp_config = config_mix.erp_config
        assert erp_config.password is None
        assert erp_config.database is None
        assert erp_config.username is None
        assert erp_config.server_name is None
        assert erp_config.cust_sort_code is None
        assert erp_config.use_cust_id_as_sort_code is False

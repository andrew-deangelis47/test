from globalshop.client import GlobalShopClient
from baseintegration.integration import logger


class GlobalShopConfig:
    def __init__(self):
        self.use_cust_id_as_sort_code = True
        self.cust_sort_code = None
        self.cust_code = None
        self.set_cust_code_on_routers = True
        self.username = None
        self.password = None
        self.database = None
        self.server_name = None
        self.run_document_control_exporter = False

        logger.info('Setup Default GlobalShopConfig')


class GlobalShopConfigMixin:
    """
    To be used with GlobalShop importers and exporters to setup the Global
    Shop configuration in a standard way.
    """
    erp_name = 'GlobalShop'

    def __init__(self, integration):
        self._integration = integration
        super().__init__(integration)

    def _setup_erp_client(self):
        GlobalShopClient(server_name=self.erp_config.server_name,
                         username=self.erp_config.username,
                         password=self.erp_config.password,
                         database=self.erp_config.database
                         )
        logger.info('Setup GlobalShopClient')

    def _setup_erp_config(self):
        self.erp_config = GlobalShopConfig()

        parser = self._integration.config_yaml["GlobalShop"]
        secrets = self._integration.secrets['GlobalShop']

        self.erp_config.use_cust_id_as_sort_code = parser.get(
            "use_cust_id_as_sort_code", False)
        self.erp_config.username = secrets.get('username')
        self.erp_config.password = secrets.get('password')
        self.erp_config.database = secrets.get('database')
        self.erp_config.server_name = secrets.get('server_name')
        self.erp_config.run_document_control_exporter = parser.get("run_document_control_exporter", False)
        self.erp_config.osv_description_var = parser.get('osv_description_var', 'Powder Description')
        self.erp_config.project_group_var = parser.get('project_group_var', 'Powder Name')
        self.erp_config.material_id_var = parser.get('material_id_var', 'Material Selection')
        self.erp_config.material_desc_var = parser.get('material_desc_var', 'Material Description')
        self.erp_config.workcenter_var = parser.get('workcenter_var', 'Workcenter Lookup')
        self.erp_config.product_line_var = parser.get('product_line_var', 'Product line')

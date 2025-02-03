from baseintegration.integration import Integration


class GlobalShopIntegration(Integration):

    def __init__(self):
        class GlobalShopConfig:
            def __init__(self):
                self.use_cust_id_as_sort_code = True
                self.cust_sort_code = None
                self.set_cust_code_on_routers = True
                self.username = None
                self.password = None
                self.database = None
                self.server_name = None
        self.erp_config = GlobalShopConfig()
        super().__init__()

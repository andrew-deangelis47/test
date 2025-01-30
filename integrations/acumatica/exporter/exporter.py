from paperless.objects.orders import Order

from baseintegration.exporter.order_exporter import OrderExporter

from acumatica.client import AcumaticaClient
from acumatica.utils import AcumaticaConfig
from acumatica.api_models.acumatica_models import SalesOrderDetail, SalesOrderHeader, StockItem, ProductionOrder, \
    ProductionOrderDetail, Operation, Customer

from acumatica.exporter.processors.customer import CustomerProcessor
from acumatica.exporter.processors.stock_item import StockItemProcessor
from acumatica.exporter.processors.production_order import ProductionOrderProcessor
from acumatica.exporter.processors.production_order_details import ProductionOrderDetailProcessor
from acumatica.exporter.processors.operation import OperationProcessor
from acumatica.exporter.processors.sales_order_header import SalesOrderHeaderProcessor
from acumatica.exporter.processors.sales_order_detail import SalesOrderDetailProcessor


class AcumaticaOrderExporter(OrderExporter):

    def _register_default_processors(self):
        self.register_processor(Customer, CustomerProcessor)
        self.register_processor(StockItem, StockItemProcessor)
        self.register_processor(ProductionOrder, ProductionOrderProcessor)
        self.register_processor(ProductionOrderDetail, ProductionOrderDetailProcessor)
        self.register_processor(Operation, OperationProcessor)
        self.register_processor(SalesOrderHeader, SalesOrderHeaderProcessor)
        self.register_processor(SalesOrderDetail, SalesOrderDetailProcessor)

    def _setup_erp_client(self):
        if not self._integration.test_mode:  # pragma: no cover
            base_url = self._integration.secrets["Acumatica"]["base_url"]
            tenant = self._integration.secrets["Acumatica"]["tenant"]
            username = self._integration.secrets["Acumatica"]["username"]
            password = self._integration.secrets["Acumatica"]["password"]
            default_endpoint = self._integration.secrets["Acumatica"]["default_endpoint"]
            mfg_endpoint = self._integration.secrets["Acumatica"]["mfg_endpoint"]
            bearer_token = self._integration.secrets["Acumatica"]["bearer_token"]
            client_id = self._integration.secrets["Acumatica"]["client_id"]
            client_secret = self._integration.secrets["Acumatica"]["client_secret"]
            ny_client_id = self._integration.secrets["Acumatica"]["ny_client_id"]
            ny_client_secret = self._integration.secrets["Acumatica"]["ny_client_secret"]
            florida_username = self._integration.secrets["Acumatica"]["florica_username"]

            # Todo: This doesn't actually test if client is valid, its going to be a silent failure
            self.client = AcumaticaClient(base_url=base_url, username=username, password=password, tenant=tenant,
                                          default_endpoint=default_endpoint, mfg_endpoint=mfg_endpoint,
                                          bearer_token=bearer_token, client_id=client_id, client_secret=client_secret,
                                          ny_client_id=ny_client_id,
                                          ny_client_secret=ny_client_secret,
                                          florida_username=florida_username)
        else:
            self.client = AcumaticaClient(api_key="test", base_url="http://testapi.com", username="test",
                                          password="test")
        self._integration.api_client = self.client

    def _setup_erp_config(self):
        if self._integration.test_mode:  # pragma: no cover
            self._set_test_mode_config_defaults()
        else:
            if not self.erp_config:
                self.erp_config = AcumaticaConfig()

    def _set_test_mode_config_defaults(self):
        """
        Use this class to set default values for test cases.
        """
        if not self.erp_config:
            self.erp_config = AcumaticaConfig()

    def _process_order(self, order: Order):
        pass

from baseintegration.exporter.order_exporter import OrderExporter, logger
from sage.exporter.processors.bom import BomProcessor
from sage.exporter.processors.part import PartProcessor
from sage.exporter.processors.customer import CustomerProcessor
from sage.exporter.processors.sales_quote import SalesQuoteProcessor
from sage.exporter.processors.routing import RoutingProcessor

from sage.models.sage_models.bom.bom_full_entity import BomFullEntity as BOM
from sage.models.sage_models.customer import Customer
from sage.models.sage_models.part import PartFullEntity
from sage.models.sage_models.routing.routing_full_entity import RoutingFullEntity as Routing
from sage.models.sage_models.sales_quote import SalesQuote

from paperless.objects.orders import Order

from sage.sage_api.client import SageImportClient
from sage.sage_config import SageConfig


class SageOrderExporter(OrderExporter):

    def _register_default_processors(self):
        self.register_processor(BOM, BomProcessor)
        self.register_processor(Routing, RoutingProcessor)
        self.register_processor(Customer, CustomerProcessor)
        self.register_processor(PartFullEntity, PartProcessor)
        self.register_processor(SalesQuote, SalesQuoteProcessor)

    def _process_order(self, order: Order):
        logger.info(f"Processing order {order.number} to quote")
        with self.process_resource(Customer, order) as customer:
            pass

        # if the customer does not exist in Sage, we cannot process this order
        if customer is None:
            return

        with self.process_resource(PartFullEntity, order) as line_item_data:
            pass
        with self.process_resource(BOM, order):
            pass
        with self.process_resource(Routing, order):
            pass
        with self.process_resource(SalesQuote, order, line_item_data):
            pass

    def _setup_erp_client(self):
        if not self._integration.test_mode:
            api_url = self._integration.secrets["Sage"]["base_url"]
            username = self._integration.secrets["Sage"]["username"]
            password = self._integration.secrets["Sage"]["password"]
            # Todo: This doesn't actually test if client is valid, its going to be a silent failure
            self.client = SageImportClient(base_url=api_url, username=username, password=password)
        else:
            self.client = SageImportClient(api_key="test", base_url="http://testapi.com", username="test",
                                           password="test")
        self._integration.api_client = self.client

    def _setup_erp_config(self):
        if self._integration.test_mode:
            self._set_test_mode_config_defaults()
        else:
            self._set_production_erp_config()

    def _set_production_erp_config(self):
        """
        This function is responsible for assigning the Epicor 'erp_config' options from the config.yaml file.
        Add new config options here with reverse-compatible defaults specified.
        """
        order_export_yaml = self._integration.config_yaml["Exporters"]["orders"]
        if not self.erp_config:
            self.erp_config = SageConfig()
            self.erp_config.should_create_customer = order_export_yaml.get("should_create_customer", False)
            self.erp_config.default_customer_id = 'C10000'
            self.erp_config.pp_mat_id_variable = order_export_yaml.get("pp_mat_id_variable", False)
            self.erp_config.default_manufactured_class_id = order_export_yaml.get("default_manufactured_class_id", False)
            self.erp_config.company_name = order_export_yaml.get("company_name", False)
            self.erp_config.duplicate_part_number_append_character = order_export_yaml.get("duplicate_part_number_append_character", False)

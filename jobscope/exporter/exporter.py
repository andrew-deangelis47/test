from baseintegration.exporter.order_exporter import OrderExporter
from paperless.objects.orders import Order
from jobscope.client import JobscopeClient
from jobscope.exporter.processors.customer import CustomerProcessor
from jobscope.exporter.processors.part import PartProcessor
from jobscope.exporter.processors.routing import RoutingProcessor
from jobscope.exporter.processors.bom import BOMProcessor
from jobscope.exporter.processors.job import JobProcessor
from jobscope.utils import Customer, Part, Routing, BOM, Job
from baseintegration.datamigration import logger


class JobscopeOrderExporter(OrderExporter):

    def _register_default_processors(self):
        self.register_processor(Customer, CustomerProcessor)
        self.register_processor(Part, PartProcessor)
        self.register_processor(Routing, RoutingProcessor)
        self.register_processor(BOM, BOMProcessor)
        self.register_processor(Job, JobProcessor)

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            api_url = self._integration.config_yaml["Jobscope"]["api_url"]
            self.client = JobscopeClient(api_url)
            username = self._integration.config["jobscope_username"]
            password = self._integration.config["jobscope_password"]
        else:
            self.client = JobscopeClient("http://testapi.com")
            username = "test"
            password = "test"
            self._integration.config_yaml["Jobscope"] = {"location_code": "HC"}
        self.client.login(username, password)
        self._integration.api_client = self.client

    def _process_order(self, order: Order):
        # login again if new order to process
        self._setup_erp_config()
        with self.process_resource(Customer, order) as customer:
            logger.info(f"Processed customer for order {order.number}")
        with self.process_resource(Part, order) as parts:
            logger.info(f"Processed parts for order {order.number}")
        with self.process_resource(Routing, parts):
            logger.info(f"Processed routing for order {order.number}")
        with self.process_resource(BOM, parts):
            logger.info(f"Processed BOM for order {order.number}")
        with self.process_resource(Job, order, customer):
            logger.info(f"Processed job for order {order.number}")

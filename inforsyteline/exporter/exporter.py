from baseintegration.exporter.order_exporter import OrderExporter
from paperless.objects.orders import Order
from inforsyteline.models import CustomerMst, ItemMst, JobmatlMst, JobrouteMst, CoMst
from inforsyteline.exporter.processors.customer import CustomerProcessor
from inforsyteline.exporter.processors.item import ItemProcessor
from inforsyteline.exporter.processors.job_route import JobRouteProcessor
from inforsyteline.exporter.syteline_10_processors.job_route import Syteline10JobRouteProcessor
from inforsyteline.exporter.processors.job_matl import JobMatlProcessor
from inforsyteline.exporter.processors.customer_order import CustomerOrderProcessor
from baseintegration.datamigration import logger
import os
from inforsyteline.exporter.configuration import InforSytelineConfig
from inforsyteline.utils import get_version_number


class InforSytelineOrderExporter(OrderExporter):

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            logger.info('Reading config specific configuration file')
            parser = self._integration.config_yaml["Exporters"]["orders"]
            DB_NAME = os.environ.get('DB_NAME')
            self.erp_config = InforSytelineConfig(
                name=DB_NAME,
                site_ref=parser.get('site_ref'),
                pp_work_center_variable=parser.get('pp_work_center_variable'),
                fail_if_new_customer=parser.get('fail_if_new_customer', False),
                default_product_code=parser.get('default_product_code', 'HDW'),
                job_route_schedule_driver=parser.get('job_route_schedule_driver', 'L'),  # L for labor, M for machine
                job_route_backflush_type=parser.get('job_route_backflush_type', 'N')
            )
        else:
            os.environ.setdefault('TEST', '1')
            self.erp_config = InforSytelineConfig(
                name="test",
                site_ref="test",
                pp_work_center_variable="workcenter",
                fail_if_new_customer=False,
                default_product_code="HDW",
                job_route_schedule_driver="L",
                job_route_backflush_type="N"
            )

    def _register_default_processors(self):
        if get_version_number() == "syteline_10":
            self.register_processor(JobrouteMst, Syteline10JobRouteProcessor)
        else:
            self.register_processor(JobrouteMst, JobRouteProcessor)
        self.register_processor(CustomerMst, CustomerProcessor)
        self.register_processor(ItemMst, ItemProcessor)
        self.register_processor(JobmatlMst, JobMatlProcessor)
        self.register_processor(CoMst, CustomerOrderProcessor)

    def _process_order(self, order: Order):
        logger.info(f'Processing order {order.number}')
        logger.info('Testing InforSyteline Connection')
        c = CustomerMst.objects.count()
        logger.info(f"Found {c} objects")
        self.cust_num = None
        self.order = order
        # Syteline requires the usage of the SetSiteSp in order to execute any inserts. Therefore, site_ref must be set in the config
        if not self.erp_config.site_ref:
            raise ValueError("Site ref is not set. You cannot use the integration without site_ref")
        with self.process_resource(CustomerMst, order) as customer:
            self.cust_num = customer.cust_num
            logger.info("Processed customer")
        with self.process_resource(ItemMst, order) as item_processor_data:
            manufactured_components = item_processor_data.manufactured_components
            purchased_components = item_processor_data.purchased_components
            materials = item_processor_data.materials
            logger.info("Processed items")
        with self.process_resource(JobrouteMst, manufactured_components):
            logger.info("Processed job routes")
        with self.process_resource(JobmatlMst, manufactured_components, purchased_components, materials):
            logger.info("Processed job materials")
        with self.process_resource(CoMst, order, customer):
            logger.info("Processed customer order")
        logger.info("Done processing order!")

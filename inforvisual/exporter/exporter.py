from baseintegration.datamigration import logger
from paperless.objects.orders import Order
from inforvisual.exporter.configuration import InforVisualConfig
from inforvisual.exporter.processors.account import AccountProcessor
from inforvisual.exporter.processors.customer import CustomerProcessor
from inforvisual.exporter.processors.part import PartProcessor
from inforvisual.exporter.processors.operation import OperationProcessor
from inforvisual.exporter.processors.work_order import WorkOrderProcessor
from inforvisual.exporter.processors.requirement import RequirementProcessor
from inforvisual.exporter.processors.customer_order import \
    CustomerOrderProcessor
from baseintegration.exporter.order_exporter import OrderExporter
from inforvisual.models import Customer, Part, WorkOrder, Operation, \
    Requirement, CustomerOrder
import os


class InforVisualOrderExporter(OrderExporter):
    """An integration specific to infor visual"""

    def _setup_erp_config(self):
        if not self._integration.test_mode:
            logger.info('Reading config specific configuration file')
            parser = self._integration.config_yaml["Exporters"]["orders"]
            DB_HOST = os.environ.get('DB_HOST')
            DB_INSTANCE = os.environ.get('DB_INSTANCE')
            DB_PORT = os.environ.get('DB_PORT', '1433')
            DB_NAME = os.environ.get('DB_NAME')
            DB_USERNAME = os.environ.get('DB_USERNAME', 'sa')
            DB_PASSWORD = os.environ.get('DB_PASSWORD')
            self.erp_config = InforVisualConfig(
                host=DB_HOST,
                instance=DB_INSTANCE,
                port=DB_PORT,
                name=DB_NAME,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                paperless_user=parser.get('paperless_user'),
                email_password=parser.get('email_password'),
                update_customers=parser.get("update_customers", True),
                send_email_when_customer_not_found=parser.get(
                    'send_email_when_customer_not_found', False),
                vendor_variable=parser.get('vendor_variable',
                                           'Workcenter Lookup'),
                pp_mat_id_variable=parser.get('pp_mat_id_variable',
                                              'Workcenter Lookup'),
                default_site_id=parser.get('default_site_id', 'SITE'),
                create_purchased_component=parser.get(
                    'create_purchased_component', False),
                create_material=parser.get('create_purchased_component',
                                           False),
                leg_assembly=parser.get('leg_assembly', True),
                pp_parts_per_material_unit_variable=parser.get(
                    'pp_parts_per_material_unit_variable',
                    'Parts Per Material Stock Unit'),
                vendor_id_var=parser.get('vendor_id_var'),
                service_id_var=parser.get('service_id_var'),
                service_min_chg_var=parser.get('service_min_chg_var'),
                run_cost_per_unit_var=parser.get('run_cost_per_unit_var'),
                transit_days_var=parser.get('transit_days_var'),
                work_center_var=parser.get('work_center_var'),
                should_export_assemblies_with_duplicate_components=parser.get(
                    "should_export_assemblies_with_duplicate_components", False
                )
            )
        else:
            os.environ.setdefault('TEST', '1')
            self.erp_config = InforVisualConfig(
                host="test",
                instance="test",
                port=0,
                name="test",
                user="test",
                password="test",
                paperless_user="test",
                email_password="test",
                update_customers=True,
                send_email_when_customer_not_found=False,
                pp_mat_id_variable="workcenter",
                default_site_id="MTI",
                create_material=True,
                pp_parts_per_material_unit_variable="test",
                create_purchased_component=True,
                leg_assembly=True,
                vendor_id_var='test',
                service_id_var='test',
                service_min_chg_var='test',
                run_cost_per_unit_var='test',
                transit_days_var='test',
                work_center_var='test',
                should_export_assemblies_with_duplicate_components=False
            )

    def _register_default_processors(self):
        self.register_processor(Customer, CustomerProcessor)
        self.register_processor(Part, PartProcessor)
        self.register_processor(WorkOrder, WorkOrderProcessor)
        self.register_processor(Operation, OperationProcessor)
        self.register_processor(Requirement, RequirementProcessor)
        self.register_processor(CustomerOrder, CustomerOrderProcessor)

    def _process_order(self, order: Order):
        logger.info(f'Processing order {order.number}')
        logger.info('Testing INFORVISUAL Connection')
        c = Customer.objects.count()
        logger.info(f'Estim count: {str(c)} OK!')
        account_id, business_name, contact_id, customer_notes, erp_code, payment_terms, payment_terms_period, billing_info = \
            self.get_account_data(order)

        with self.process_resource(Customer, business_name, erp_code,
                                   account_id, payment_terms,
                                   payment_terms_period,
                                   contact_id, billing_info,
                                   order.number) as customer_data:
            logger.info("Customer has been processed")

            with self.process_resource(Part, order) as part_processor_data:
                part_data: list = part_processor_data.part_data
                material_data: list = part_processor_data.material_data
                order_item_data: list = part_processor_data.order_item_data
                logger.info("Parts have been processed")

                with self.process_resource(WorkOrder, order, part_data,
                                           order_item_data) as work_orders_and_components:
                    work_orders: list = work_orders_and_components[0]
                    purchased_components: list = work_orders_and_components[1]
                    logger.info("Work orders have been processed")
                    logger.info(
                        f"Number of work orders is {str(len(work_orders))}")

                    with self.process_resource(Operation, order, work_orders):
                        logger.info("Operations have been processed")

                        with self.process_resource(Requirement, order,
                                                   work_orders,
                                                   purchased_components,
                                                   material_data):
                            logger.info("Requirements have been processed")

                            with self.process_resource(CustomerOrder, order,
                                                       customer_data.customer,
                                                       part_data,
                                                       order_item_data):
                                logger.info(
                                    "Customer orders have been processed")
                                logger.info(
                                    f"Done processing order number {order.number}")

    @staticmethod
    def get_account_data(order: Order):
        business_name, erp_code, payment_terms, payment_terms_period, customer_notes, account_id, contact_id, billing_info = \
            AccountProcessor.process_account_info(order)
        return account_id, business_name, contact_id, customer_notes, erp_code, payment_terms, payment_terms_period, billing_info

from baseintegration.exporter.order_exporter import OrderExporter
from paperless.objects.orders import Order
from e2_cloud.exporter.processors.customer import CustomerProcessor
from e2_cloud.exporter.processors.bom import BOMProcessor
from paperless.objects.customers import Account


class E2CloudOrderExporter(OrderExporter):

    def _register_default_processors(self):
        self.register_processor(Account, CustomerProcessor)
        self.register_processor(Order, BOMProcessor)

    def _setup_erp_config(self):
        class E2CloudConfig:

            def __init__(self):
                self.pp_mat_id_variable = None
        self.erp_config = E2CloudConfig()

    def _process_order(self, order: Order) -> list:
        account = Account.get(order.contact.account.id)
        with self.process_resource(Account, account):
            pass
        with self.process_resource(Order, order) as item_list:
            pass
        return item_list

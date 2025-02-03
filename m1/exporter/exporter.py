from baseintegration.exporter.order_exporter import OrderExporter
from paperless.objects.orders import Order
from m1.exporter.processors.organizations import ProcessOrganization
from m1.exporter.processors.sales_orders import ProcessSalesOrder
from m1.exporter.processors.sales_order_lines import ProcessMakePartSalesOrderLines, SalesOrderAddOn, \
    SalesOrderExpedite, ProcessAddOnSalesOrderLines, ProcessExpediteSalesOrderLines
from m1.exporter.processors.jobs import ProcessJobs
from m1.models import Salesorders, Salesorderlines, Jobs, Organizations
from m1.configureation import ERPConfigFactory


class M1OrderExporter(OrderExporter):

    def _setup_erp_config(self):
        self.erp_config = ERPConfigFactory.create_config(self._integration)

    def _register_default_processors(self):
        self.register_processor(Organizations, ProcessOrganization)
        self.register_processor(Salesorders, ProcessSalesOrder)
        self.register_processor(Salesorderlines, ProcessMakePartSalesOrderLines)
        self.register_processor(SalesOrderAddOn, ProcessAddOnSalesOrderLines)
        self.register_processor(SalesOrderExpedite, ProcessExpediteSalesOrderLines)
        self.register_processor(Jobs, ProcessJobs)

    def _process_order(self, order: Order):
        with self.process_resource(Organizations, order) as buyer_org:
            if buyer_org is False:
                return False
            with self.process_resource(Salesorders, order, buyer_org) as new_sales_order:
                order_item_index = 1
                if new_sales_order is False:
                    return False
                for item in order.order_items:
                    with self.process_resource(Salesorderlines, order, new_sales_order, item,
                                               order_item_index) as new_sales_order_line:
                        with self.process_resource(Jobs, order, new_sales_order, new_sales_order_line, item,
                                                   order_item_index):
                            pass
                    for addon in item.ordered_add_ons:
                        order_item_index += 1
                        with self.process_resource(SalesOrderAddOn, order, new_sales_order, addon, order_item_index):
                            pass
                    if item.expedite_revenue:
                        order_item_index += 1
                        with self.process_resource(SalesOrderExpedite, order, new_sales_order,
                                                   item.expedite_revenue, order_item_index):
                            pass
                    order_item_index += 1
                return True

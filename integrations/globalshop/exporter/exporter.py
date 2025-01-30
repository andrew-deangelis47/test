from globalshop.client import GlobalShopClient
from globalshop.discount_table import DiscountTable
from globalshop.cross_reference import CrossReference
from globalshop.document_control import DocumentControl
from globalshop.exporter.processors.discount_table import DiscountTableProcessor
from globalshop.exporter.processors.cross_reference import CrossReferenceProcessor
from globalshop.exporter.processors.document_control import DocumentControlProcessor
from globalshop.customer import Customer
from paperless.objects.orders import Order as PPOrder
from baseintegration.integration import logger
from globalshop.bom import BOM
from globalshop.exporter.processors.part import PartProcessor
from globalshop.exporter.processors.router import RouterProcessor
from globalshop.integration.config_mixin import GlobalShopConfigMixin
from globalshop.order import OrderLine
from baseintegration.exporter.order_exporter import OrderExporter
from globalshop.exporter.processors.order_line import OrderLineProcessor
from globalshop.exporter.processors.bom import BOMProcessor
from globalshop.router import Router
from globalshop.part import Part
from globalshop.addon import AddOnRecord
from globalshop.exporter.processors.add_on_charge import AddOnProcessor


class GlobalShopOrderExporter(GlobalShopConfigMixin, OrderExporter):

    def _process_order(self, order: PPOrder) -> bool:
        # Ensure the customer exists:
        # TODO: create Customer Exporter

        contact = order.contact
        account = contact.account
        if account:
            erp_code = account.erp_code
            logger.debug(f'{erp_code}')
        else:
            pass

        customer_record = Customer.get(erp_code)
        if customer_record is not None:
            gss_cust_number = customer_record.gss_customer_number if customer_record.gss_customer_number is not None else ''
            logger.debug(f'Retrieve Customer record based on erp_code of "'
                         f'{erp_code}", found {customer_record} with gss_id of '
                         f'{gss_cust_number}')

        # Export the Order one line at a time
        logger.info(f"Processing Paperless Parts Order: {order.number}")
        line_number = 0
        for order_item in order.order_items:
            line_number += 1
            with self.process_resource(OrderLine, order, order_item, line_number, customer_record):
                pass
            for add_on in order_item.ordered_add_ons:
                line_number += 1
                with self.process_resource(AddOnRecord, order, order_item, line_number, customer_record):
                    pass
        client: GlobalShopClient = GlobalShopClient.get_instance()
        client.execute_cache(commit=True)
        for order_item in order.order_items:
            with self.process_resource(Part, order_item, order, customer_record):
                pass
            with self.process_resource(CrossReference, order_item, order, customer_record):
                pass
            with self.process_resource(DocumentControl, order_item, order):
                pass
            with self.process_resource(DiscountTable, order_item, order):
                pass
            with self.process_resource(BOM, order_item):
                pass
            with self.process_resource(Router, order_item, customer_record):
                pass

        return True

    def _register_default_processors(self):
        self.register_processor(OrderLine, OrderLineProcessor)
        self.register_processor(BOM, BOMProcessor)
        self.register_processor(Router, RouterProcessor)
        self.register_processor(Part, PartProcessor)
        self.register_processor(CrossReference, CrossReferenceProcessor)
        self.register_processor(DocumentControl, DocumentControlProcessor)
        self.register_processor(DiscountTable, DiscountTableProcessor)
        self.register_processor(AddOnRecord, AddOnProcessor)

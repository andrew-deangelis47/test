import datetime
from typing import Optional

from baseintegration.datamigration import logger
from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order, OrderItem, OrderComponent

from m2m.exporter.processors.quote_bom import QuoteBOMFactory
from m2m.exporter.processors.quote_router import QuoteRouterFactory
from m2m.exporter.processors.sales_quotes import SalesQuoteFactory
from m2m.exporter.processors.standard_bom import StandardBOMFactory
from m2m.exporter.processors.standard_router import RouterFactory
from m2m.exporter.processors.sales_orders import SalesOrderFactory
from m2m.configuration import M2MConfiguration
from m2m.utils.item_master import ItemMasterHelper
import m2m.models as mm

DEFAULT_DATE = datetime.datetime(1900, 1, 1, 0, 0, 0)


class ProcessOrder(BaseProcessor):
    m2m_config = M2MConfiguration()
    bom_factory = None
    router_factory = None
    sales_order_factory = None
    sales_quote_factory = None

    def _process(self, order: Order, config: M2MConfiguration):
        self.m2m_config = config

        if self.m2m_config.export_as_quote:
            self.export_order_to_quote(order)
        else:
            self.export_order_to_sales_order(order)

    def export_order_to_sales_order(self, order: Order):
        self.bom_factory = StandardBOMFactory(configuration=self.m2m_config)
        self.router_factory = RouterFactory(configuration=self.m2m_config)
        self.sales_order_factory = SalesOrderFactory(configuration=self.m2m_config)

        # get customer ERP code
        if self.m2m_config.create_m2m_accounts:
            raise NotImplementedError
        elif self.m2m_config.default_erp_code is None:
            raise TypeError
        else:
            erp_code = order.contact.account.erp_code if order.contact.account and order.contact.account.erp_code \
                else self.m2m_config.default_erp_code

        # create items, standard BOMs, and standard routings for each order item
        for order_item in order.order_items:
            components = self.get_component_id_to_data_map(order_item)
            consolidate = self.get_component_to_consolidate(order_item)
            notes = order_item.public_notes or ""
            self.recursive_seed_standard_bom_router(
                root=order_item.root_component,
                components=components,
                customer_erp=erp_code,
                consolidate=consolidate,
                notes=notes
            )

        # create sales order
        logger.info('create sales order')
        so_master = self.sales_order_factory.create_sales_order(
            order=order, expedite_part_number=self.m2m_config.expedite_part_number
        )

        self._exporter.success_message = f"Associated M2M sales order number is {so_master.fsono}"

    def export_order_to_quote(self, order: Order):
        self.bom_factory = QuoteBOMFactory(configuration=self.m2m_config)
        self.router_factory = QuoteRouterFactory(configuration=self.m2m_config)
        self.sales_quote_factory = SalesQuoteFactory(configuration=self.m2m_config)

        # create quote
        logger.info('create sales quote')
        quote_master, order_item_to_quote_item = self.sales_quote_factory.create_sales_quote(
            order=order
        )

        # create quote BOMs and quote routings for each non-standard quote item
        for order_item in order.order_items:
            quote_item, price_summary, root_bom_line = order_item_to_quote_item[order_item.id]
            quote_item: mm.Qtitem
            price_summary: mm.Qtpest  # each quote item has an associated price summary that we must update with prices
            root_bom_line: mm.Qtdbom  # each quote item has a root BOM line (it is not shown in the UI)
            if not quote_item.fstandpart:
                logger.info(f'Building BOM and router for order item: {order_item.root_component.part_name}')
                components = self.get_component_id_to_data_map(order_item)
                consolidate = self.get_component_to_consolidate(order_item)
                self.recursive_seed_quote_bom_router(
                    root=order_item.root_component,
                    components=components,
                    order_item=order_item,
                    m2m_quote_item=quote_item,
                    consolidate=consolidate,
                    price_summary=price_summary,
                    bom_line=root_bom_line
                )
            else:
                logger.info(f'Using standard BOM and routing for order item: {order_item.root_component.part_name}')

        self._exporter.success_message = f"Associated M2M sales quote number is {quote_master.fquoteno}"

    def get_component_to_consolidate(self, order_item: OrderItem) -> Optional[int]:
        item_id = None
        primary_component: OrderComponent
        make_count = 0
        consolidate = None
        for item in order_item.components:
            if self.m2m_config.enable_part_consolidation:
                for op in item.shop_operations:
                    if item.type != "purchased" and op.operation_definition_name == 'CONSOLIDATE':
                        consolidate = item.id
                        logger.info(
                            f"Consolidating assembly via Operation check.  Sub component {consolidate} will"
                            f" roll up to its parent")
                        break
                if item.type != "purchased" and item.id != order_item.root_component_id:
                    make_count += 1
                    item_id = item.id
        if consolidate is None and make_count == 1 and item_id is not None:
            consolidate = item_id
            logger.info(
                f"Consolidating assembly via Single Make Par condition.  Sub component {consolidate} will "
                f"roll up to its parent")
        return consolidate

    def get_component_id_to_data_map(self, order_item: OrderItem):
        components = {}
        for item in order_item.components:
            components[item.id] = item
        return components

    def recursive_seed_standard_bom_router(self, root: OrderComponent, components: {OrderComponent}, customer_erp: str,
                                           consolidate: int = None, notes: str = ''):
        self.bom_factory: StandardBOMFactory
        self.router_factory: RouterFactory

        if root.type == "purchased":
            return

        for child in root.child_ids:
            if consolidate != child:
                self.recursive_seed_standard_bom_router(components[child], components, customer_erp)

        logger.info(f'check item master: {root.part_number}')
        item_record = ItemMasterHelper.check_create_item_for_make(root, customer_erp, notes)
        logger.info('create router')
        ops = self.router_factory.check_create_standard_routers(item_record, root, components, consolidate)
        logger.info('create bom')
        self.bom_factory.check_create_standard_bom(item_record, root, components, ops, consolidate)

    def recursive_seed_quote_bom_router(
            self, root: OrderComponent, components: {OrderComponent}, order_item: OrderItem,
            m2m_quote_item: mm.Qtitem, price_summary: mm.Qtpest, bom_line: mm.Qtdbom, consolidate: int = None,
            largest_bom_item_num=0, level=1
    ):
        self.bom_factory: QuoteBOMFactory
        self.router_factory: QuoteRouterFactory

        if root.type == "purchased":
            return largest_bom_item_num

        logger.info('create quote bom')
        largest_bom_item_num, child_component_bom_lines = self.bom_factory.check_create_quote_bom(
            bom_line=bom_line, root=root, components=components, order_item=order_item,
            m2m_quote_item=m2m_quote_item, level=level, price_summary=price_summary,
            last_bom_item_num=largest_bom_item_num, consolidate=consolidate
        )

        logger.info('create quote router')
        self.router_factory.check_create_quote_routers(
            bom_line=bom_line, comp=root, components=components, m2m_quote_item=m2m_quote_item,
            price_summary=price_summary, consolidate=consolidate
        )

        for child_id, child_bom_line in child_component_bom_lines:
            largest_bom_item_num = self.recursive_seed_quote_bom_router(
                root=components[child_id], components=components, order_item=order_item,
                m2m_quote_item=m2m_quote_item, price_summary=price_summary, consolidate=consolidate,
                bom_line=child_bom_line, largest_bom_item_num=largest_bom_item_num, level=level + 1
            )

        return largest_bom_item_num

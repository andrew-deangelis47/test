from baseintegration.datamigration import logger
from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order, OrderItem, OrderedAddOn
from m1.exporter.processors.utils import PartUtils, SalesOrderUtils, NoteUtils
from m1.models import Salesorders
from paperless.objects.common import Money


class ProcessMakePartSalesOrderLines(BaseProcessor):

    def _process(self, order: Order, new_sales_order: Salesorders, item: OrderItem, idx: int):
        line_item_notes = NoteUtils.get_line_item_notes(item=item)

        part, rev = PartUtils.get_create_component_part(component=item.root_component, long_description=line_item_notes)
        qty = item.quantity
        unit_cost = item.unit_price.raw_amount
        new_line = SalesOrderUtils.create_line_item(idx=idx, new_sales_order=new_sales_order, part=part, rev=rev,
                                                    qty=qty, unit_cost=unit_cost)
        SalesOrderUtils.create_delivery(idx=idx, new_sales_order=new_sales_order, part=part, rev=rev, qty=qty,
                                        delivery_date=order.ships_on_dt)
        logger.info(f'Created Sales Order Line Item Record in M1 for for quote item: {part.imppartid}')
        return new_line


class ProcessAddOnSalesOrderLines(BaseProcessor):

    def _process(self, order: Order, new_sales_order: Salesorders, addon: OrderedAddOn, idx: int):
        part, rev = PartUtils.get_create_placeholder_parts(part_number=f'PP-AddOn:{addon.name}',
                                                           long_description=addon.notes if addon.notes else '')

        new_line = SalesOrderUtils.create_line_item(idx=idx, new_sales_order=new_sales_order, part=part, rev=rev,
                                                    qty=1, unit_cost=addon.price.raw_amount)
        SalesOrderUtils.create_delivery(idx=idx, new_sales_order=new_sales_order, part=part, rev=rev, qty=1,
                                        delivery_date=order.ships_on_dt)
        logger.info(f'Created Sales Order Line Item Record in M1 for for add on: {addon.name}')
        return new_line


class ProcessExpediteSalesOrderLines(BaseProcessor):

    def _process(self, order: Order, new_sales_order: Salesorders, cost: Money, idx: int):
        des = 'This is a placeholder parts for a charge to get a sales order item completed faster'
        part, rev = PartUtils.get_create_placeholder_parts(part_number='PP-Expedite',
                                                           long_description=des)
        new_line = SalesOrderUtils.create_line_item(idx=idx, new_sales_order=new_sales_order, part=part, rev=rev,
                                                    qty=1, unit_cost=cost.raw_amount)
        SalesOrderUtils.create_delivery(idx=idx, new_sales_order=new_sales_order, part=part, rev=rev, qty=1,
                                        delivery_date=order.ships_on_dt)
        logger.info('Created Sales Order Line Item Record in M1 for for expedite')
        return new_line


class SalesOrderAddOn:
    pass


class SalesOrderExpedite:
    pass

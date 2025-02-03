from decimal import Decimal
from typing import List, Tuple, Optional

from baseintegration.datamigration import logger
from baseintegration.utils.test_utils import get_quote
from globalshop.discount_table import DiscountTable
from globalshop.customer import CustomerRecord
from paperless.objects.components import BaseOperation
from paperless.objects.orders import OrderItem, OrderComponent, Order
from globalshop.exporter.processors import GSProcessor


class DiscountTableProcessor(GSProcessor):

    def _process(self, item: OrderItem, order: Order,
                 customer_record: CustomerRecord = None):

        """
        We are going to write out the part level information every time,
        as the settings for when to update/insert a record is controlled
        inside Global Shop
        """
        root = item.root_component

        for assm_component in item.iterate_assembly():
            self._insert_component_discount_table(root, assm_component.component,
                                                  item, order, customer_record)

    def get_discount_types(self, component: OrderComponent):
        discount_types = ['IQD']
        for op in component.shop_operations:
            if op.operation_definition_name == 'LPF-KC' or op.operation_definition_name == 'LPF-LAN':
                discount_types.append('MQD')
        return discount_types

    def get_part_description(self, component: OrderComponent):
        if component.description is not None:
            discount_description = component.description
        else:
            return None
        return discount_description

    def get_quantities_from_op(self, component: OrderComponent) -> List[BaseOperation.OperationQuantity]:
        for op in component.shop_operations:
            if op.operation_definition_name == 'LPF-KC' or op.operation_definition_name == 'LPF-LAN':
                return op.quantities

    def get_qty_and_price_from_comp(self, component: OrderComponent, order: Order, line_item: OrderItem):
        quote_number = order.quote_number
        quote_rev = order.quote_revision_number
        quote = get_quote(quote_number, quote_rev)
        for quote_item in quote.quote_items:
            for comp in quote_item.components:
                if comp.part_number == component.part_number:
                    comp_quantities = comp.quantities
                    logger.debug(f'comp quantities {comp_quantities}')
                    return comp_quantities

    def get_qty_and_price_or_none(self, component: OrderComponent, order: Order, line_item: OrderItem,
                                  discount_type: str, index: int) -> Tuple[Optional[int], Optional[Decimal]]:
        if discount_type == 'IQD':
            quantities = self.get_qty_and_price_from_comp(component, order, line_item)
            if len(quantities) > index:
                quantity = quantities[index].quantity
                return quantity, quantities[index].unit_price.raw_amount
        else:
            quantities = self.get_quantities_from_op(component)
            if len(quantities) > index:
                quantity = quantities[index].quantity
                return quantity, quantities[index].price.raw_amount / quantity
        return None, None

    def _insert_component_discount_table(self, root: OrderComponent,
                                         component: OrderComponent,
                                         line_item: OrderItem,
                                         order: Order = None,
                                         customer_record: CustomerRecord = None):

        discount_types = self.get_discount_types(component)
        logger.debug(f'discount types {discount_types}')
        external_id = component.part_number
        partnumber = component.part_number
        revision = component.revision if component.revision else None
        location = ''
        price_date = None  # defaults to today's date
        description = self.get_part_description(component)
        for discount_type in discount_types:
            quantity_1, price_1 = self.get_qty_and_price_or_none(component, order, line_item, discount_type, 0)
            quantity_2, price_2 = self.get_qty_and_price_or_none(component, order, line_item, discount_type, 1)
            quantity_3, price_3 = self.get_qty_and_price_or_none(component, order, line_item, discount_type, 2)
            quantity_4, price_4 = self.get_qty_and_price_or_none(component, order, line_item, discount_type, 3)
            quantity_5, price_5 = self.get_qty_and_price_or_none(component, order, line_item, discount_type, 4)
            quantity_6, price_6 = self.get_qty_and_price_or_none(component, order, line_item, discount_type, 5)
            quantity_7, price_7 = self.get_qty_and_price_or_none(component, order, line_item, discount_type, 6)
            quantity_8, price_8 = self.get_qty_and_price_or_none(component, order, line_item, discount_type, 7)
            quantity_9, price_9 = self.get_qty_and_price_or_none(component, order, line_item, discount_type, 8)
            quantity_10, price_10 = self.get_qty_and_price_or_none(component, order, line_item, discount_type, 9)

            DiscountTable.insert(type=discount_type,
                                 external_id=external_id,
                                 partnumber=partnumber,
                                 revision=revision,
                                 location=location,
                                 price_date=price_date,
                                 description=description,
                                 quantity_1=quantity_1,
                                 price_1=price_1,
                                 quantity_2=quantity_2,
                                 price_2=price_2,
                                 quantity_3=quantity_3,
                                 price_3=price_3,
                                 quantity_4=quantity_4,
                                 price_4=price_4,
                                 quantity_5=quantity_5,
                                 price_5=price_5,
                                 quantity_6=quantity_6,
                                 price_6=price_6,
                                 quantity_7=quantity_7,
                                 price_7=price_7,
                                 quantity_8=quantity_8,
                                 price_8=price_8,
                                 quantity_9=quantity_9,
                                 price_9=price_9,
                                 quantity_10=quantity_10,
                                 price_10=price_10
                                 )

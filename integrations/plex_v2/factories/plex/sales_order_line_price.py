from plex_v2.objects.sales_orders import SalesOrderLinePrice
from paperless.objects.orders import OrderItem
from plex_v2.factories.base import BaseFactory


class SalesOrderLinePriceFactory(BaseFactory):

    def to_sales_order_line_price(self, order_item: OrderItem) -> SalesOrderLinePrice:
        unit_name = self.config.default_sales_order_line_unit_type

        return SalesOrderLinePrice(
            currencyCode='USD',
            unit=unit_name,
            price=float(order_item.unit_price.raw_amount),
            breakpointQuantity=0
        )

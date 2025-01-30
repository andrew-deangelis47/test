from plex_v2.objects.sales_orders import SalesOrderRelease
from plex_v2.factories.base import BaseFactory
from paperless.objects.orders import OrderItem
from plex_v2.objects.sales_orders import SalesOrderLine
from datetime import timedelta, timezone


class SalesOrderReleaseFactory(BaseFactory):

    def to_sales_order_release(self, pp_order_item: OrderItem, ship_to_address_id: str, sales_order_line: SalesOrderLine) -> SalesOrderRelease:
        return SalesOrderRelease(
            quantity=pp_order_item.quantity,
            shipFrom=self.config.default_ship_from_building_code,
            status=self.config.default_sales_order_release_status,
            type=self.config.default_sales_order_release_type,
            shipToAddressId=ship_to_address_id,
            dueDate=self._get_due_date(pp_order_item),
            orderLineId=sales_order_line.id,
        )

    def _get_due_date(self, order_item: OrderItem) -> str:
        return (order_item.ships_on_dt + timedelta(
            hours=23,
            minutes=59,
            seconds=59)).replace(tzinfo=timezone(timedelta())).isoformat()

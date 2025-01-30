from plex_v2.factories.base import BaseFactory
from plex_v2.objects.sales_orders import SalesOrderLine
from plex_v2.objects.sales_orders import SalesOrder
from plex_v2.objects.unit import Unit
from plex_v2.objects.part import Part
from plex_v2.objects.customer import CustomerPart


class SalesOrderLineFactory(BaseFactory):

    def to_sales_order_line(self, part: Part, customer_part: CustomerPart, sales_order: SalesOrder) -> SalesOrder:
        # 1) create the order line
        order_line = SalesOrderLine(
            partId=part.id,
            customerPartId=customer_part.id,
            active=True,
            defaultOrderUnitId=self._get_default_order_unit_id(),
        )
        order_line.order_id = sales_order.id

        return order_line

    def _get_default_order_unit_id(self):
        """
        searches the units in plex by name and returns the id
        """
        saleas_order_line_unit_name = self.config.default_sales_order_line_unit_type
        units = Unit.find_units(unit_name=saleas_order_line_unit_name)
        for unit in units:
            if unit.unit == saleas_order_line_unit_name:
                return unit.id
        return "00000000-0000-0000-0000-000000000000"

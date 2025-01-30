from plex_v2.factories.base import BaseFactory
from plex_v2.objects.sales_orders import SalesOrderLineApprovedShipTo, SalesOrderLine


class ApprovedShipToFactory(BaseFactory):

    def to_approved_ship_to(self, ship_to_address_id: str, order_line: SalesOrderLine) -> SalesOrderLineApprovedShipTo:
        approved_ship_to = SalesOrderLineApprovedShipTo(
            shipToAddressId=ship_to_address_id,
            defaultShipFromCode=self.config.default_ship_from_building_code
        )

        approved_ship_to.order_id = order_line.order_id
        approved_ship_to.line_id = order_line.id

        return approved_ship_to

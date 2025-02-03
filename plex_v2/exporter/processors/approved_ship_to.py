from plex_v2.objects.sales_orders import SalesOrderLineApprovedShipTo, SalesOrderLine
from plex_v2.factories.plex.approved_ship_to import ApprovedShipToFactory
from plex_v2.exporter.processors.base import PlexProcessor


class ApprovedShipToProcessor(PlexProcessor):

    def _process(self, ship_to_address_id: str, order_line: SalesOrderLine, factory: ApprovedShipToFactory) -> SalesOrderLineApprovedShipTo:
        approved_ship_to: SalesOrderLineApprovedShipTo = factory.to_approved_ship_to(ship_to_address_id, order_line)
        approved_ship_to.create()

        return approved_ship_to

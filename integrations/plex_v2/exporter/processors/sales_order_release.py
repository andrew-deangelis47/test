from plex_v2.exporter.processors.base import PlexProcessor
from plex_v2.objects.sales_orders import SalesOrderRelease, SalesOrderLine
from plex_v2.factories.plex.sales_order_release import SalesOrderReleaseFactory
from paperless.objects.orders import OrderItem


class SalesOrderReleaseProcessor(PlexProcessor):
    def _process(self, order_item: OrderItem, ship_to_address_id: str, sales_order_line: SalesOrderLine, sales_order_release_factory: SalesOrderReleaseFactory) -> SalesOrderRelease:

        order_release: SalesOrderRelease = sales_order_release_factory.to_sales_order_release(
            order_item,
            ship_to_address_id,
            sales_order_line
        )

        return order_release.create()

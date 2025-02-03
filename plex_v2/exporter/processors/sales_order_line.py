from plex_v2.exporter.processors.base import PlexProcessor
from plex_v2.objects.sales_orders import SalesOrderLine, SalesOrder
from plex_v2.objects.plex_part_to_plex_customer_part_mapping import PlexPartToPlexCustomerPartMapping
from plex_v2.factories.plex.sales_order_line import SalesOrderLineFactory
from plex_v2.factories.plex.sales_order_line_price import SalesOrderLinePriceFactory
from paperless.objects.orders import OrderItem
from plex_v2.objects.part import Part
from plex_v2.objects.customer import CustomerPart
from plex_v2.objects.sales_orders import SalesOrderLinePrice


class SalesOrderLineProcessor(PlexProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'sales_order'

    def _process(self, mapping: PlexPartToPlexCustomerPartMapping, sales_order: SalesOrder, line_no: int, sales_order_line_factory: SalesOrderLineFactory, sales_order_line_price_factory: SalesOrderLinePriceFactory) -> SalesOrderLine:
        plex_part: Part = mapping.part
        plex_customer_part: CustomerPart = mapping.customer_part
        order_item: OrderItem = mapping.pp_order_item

        # 1) create sales order line model
        sales_order_line: SalesOrderLine = sales_order_line_factory.to_sales_order_line(plex_part, plex_customer_part, sales_order)

        # 2) create the line price model
        sales_order_line_price: SalesOrderLinePrice = sales_order_line_price_factory.to_sales_order_line_price(order_item)

        # 3) add line price to order line
        sales_order_line.add_line_price(sales_order_line_price)

        # 4) create the sales order and the corresponding line price
        sales_order_line.create()
        self._add_report_message(f'Created sales order line number {line_no} for PO {sales_order.poNumber}')
        return sales_order_line

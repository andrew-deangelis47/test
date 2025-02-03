from plex.exporter.processors.base import PlexProcessor
from plex.objects.sales_orders import SalesOrder, SalesOrderLineDataSource
from paperless.objects.orders import OrderItem
from plex.objects.part import Part
from plex.objects.customer import CustomerPart, Customer


class SalesOrderTier2LineProcessor(PlexProcessor):
    def _process(self, order_item: OrderItem, part: Part, customer_part: CustomerPart, sales_order: SalesOrder, date,
                 customer: Customer) -> bool:
        unit_price, qty = order_item.unit_price, order_item.quantity
        ship_date = order_item.ships_on_dt
        time_offset = int(self._exporter.erp_config.ship_date_time_offset) \
            if self._exporter.erp_config.ship_date_time_offset else 0
        ship_date = ship_date.replace(hour=(ship_date.hour + time_offset))
        ship_date_iso = ship_date.isoformat() + 'Z'
        date_offset = int(self._exporter.erp_config.ship_date_due_date_offset) \
            if self._exporter.erp_config.ship_date_time_offset else 0
        due_day = ship_date.replace(day=(date_offset + ship_date.day))
        due_date_iso = due_day.isoformat() + 'Z'

        line = SalesOrderLineDataSource(
            customerId=customer.code,
            partId=part.number,
            partRev=part.revision,
            customerPartId=customer_part.number,
            customerPartRev=customer_part.revision,
            order_id=sales_order.order_number,
            price=float(unit_price.raw_amount),
            standardPackQuantity=qty,
            c_url=self._exporter.erp_config.datasources_tier_2_line_itme,
            unit_type=self._exporter.erp_config.default_sales_order_line_unit_type,
            releaseType=self._exporter.erp_config.default_sales_order_release_type,
            releaseStatus=self._exporter.erp_config.default_sales_order_release_status,
            releaseSource=self._exporter.erp_config.default_ship_from_building_code,
            priority=self._exporter.erp_config.default_sales_order_category,
            shipDate=ship_date_iso,
            note=order_item.private_notes if order_item.private_notes else '',
            packagingNote=order_item.public_notes if order_item.public_notes else '',
            dueDate=due_date_iso
        )

        return line.create()

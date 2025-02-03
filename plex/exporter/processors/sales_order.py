from plex.exporter.processors.base import PlexProcessor
from plex.objects.sales_orders import SalesOrder, SalesOrderLine, SalesOrderLinePrice, SalesOrderRelease, \
    SalesOrderLineApprovedShipTo, SalesOrder2Tier
from paperless.objects.orders import PaymentDetails, OrderItem, Order
from paperless.objects.quotes import Quote
from plex.objects.part import Part
from plex.objects.customer import CustomerPart, Customer
from plex.objects.unit import Unit
from baseintegration.datamigration import logger


class SalesOrderLineProcessor(PlexProcessor):

    def get_default_order_unit_id(self, unit_name):
        units = Unit.find_units(unit_name=unit_name)
        for unit in units:
            if unit.unit == unit_name:
                return unit.id
        return "00000000-0000-0000-0000-000000000000"

    def _process(self, order_item: OrderItem, part: Part, customer_part: CustomerPart, sales_order: SalesOrder,
                 create=False) -> SalesOrderLine:
        unit_price, qty = order_item.unit_price, order_item.quantity

        order_line = SalesOrderLine(
            partId=part.id,
            customerPartId=customer_part.id,
            active=True,
        )
        order_line.order_id = sales_order.id
        unit_name = self._exporter.erp_config.default_sales_order_line_unit_type
        if self._exporter.erp_config.sales_order_line_use_default_order_unit_id:
            order_line.defaultOrderUnitId = self.get_default_order_unit_id(unit_name=unit_name)
        order_line.add_line_price(
            SalesOrderLinePrice(
                currencyCode='USD',
                unit=unit_name,
                price=float(unit_price.raw_amount),
                breakpointQuantity=0,  # Should this be 0, or the quantity ordered?
            )
        )
        logger.info('New sales order line: #{}: {}/{}, qty: {}'.format(
            part.number,
            unit_price,
            self._exporter.erp_config.default_sales_order_line_unit_type,
            qty
        ))

        if create:
            return order_line.create()
        else:
            return order_line


class SalesOrderReleaseProcessor(PlexProcessor):
    def _process(self, quantity, ship_to_address_id, due_date, order_id, order_line_id,
                 create=False) -> SalesOrderRelease:
        approved_ship_to = SalesOrderLineApprovedShipTo(
            shipToAddressId=ship_to_address_id,
            defaultShipFromCode=self._exporter.erp_config.default_ship_from_building_code,
        )
        approved_ship_to.order_id = order_id
        approved_ship_to.line_id = order_line_id
        approved_ship_to.create()

        order_release = SalesOrderRelease(
            quantity=quantity,
            shipFrom=self._exporter.erp_config.default_ship_from_building_code,  # or default ship from
            status=self._exporter.erp_config.default_sales_order_release_status,
            type=self._exporter.erp_config.default_sales_order_release_type,
            shipToAddressId=ship_to_address_id,
            dueDate=due_date,
            orderLineId=order_line_id,
        )

        logger.info('New approved ship-to for order ID <{}> and line ID <{}>'.format(
            order_id,
            order_line_id,
        ))

        if create:
            return order_release.create()
        else:
            return order_release


class SalesOrderProcessor(PlexProcessor):
    def _process(
            self,
            pp_order: Order,
            payment_details: PaymentDetails,
            billToAddressId: str,
            shipToAddressId: str,
            customer: Customer,
            quoteNumberWithRevision: str,
            tier: str = '3',
            create=False
    ) -> SalesOrder:
        pp_order_no = pp_order.number
        po_number = payment_details.purchase_order_number
        if po_number is None:
            po_number = 'PO Missing (PP Order {})'.format(pp_order_no)
        existing_sales_orders = SalesOrder.find_sales_orders(poNumber=po_number, customerId=customer.id)
        existing_sales_order = existing_sales_orders[0] if len(existing_sales_orders) > 0 else None

        if existing_sales_order and tier != '2':
            logger.info('Found existing customer PO with PO number {}'.format(po_number))
            return existing_sales_order
        else:
            logger.info('Creating new customer PO with PO number {}'.format(po_number))
            if tier == '2':
                quote = Quote.get(id=pp_order.quote_number, revision=pp_order.quote_revision_number)
                sales_person: str = f'{pp_order.sales_person.first_name} {pp_order.sales_person.last_name}'.upper()
                sales_order = SalesOrder2Tier(
                    PO_No=po_number,
                    Customer_Code=customer.code,
                    customerId=customer.id,
                    Bill_To_Customer_Address_Code=billToAddressId,
                    Ship_To_Customer_Address_Code=shipToAddressId,
                    Inside_Sales=sales_person,
                    Note=f'Paperless Parts Quote: https://app.paperlessparts.com/quotes/edit/{quoteNumberWithRevision} '
                         f'\n {pp_order.private_notes}',
                    Printed_Note=quote.quote_notes,
                    c_url=self._exporter.erp_config.datasources_tier_2_order,
                    Ship_From_Building_Code=self._exporter.erp_config.default_ship_from_building_code,
                    Order_Terms=payment_details.payment_terms if payment_details.payment_terms is not None
                    else 'Net 30',
                    Freight_Terms=self._exporter.erp_config.default_sales_order_freight_terms,
                    Carrier_Code=self._exporter.erp_config.default_sales_order_carrier_code,
                    PO_Category=self._exporter.erp_config.default_sales_order_category,
                )

            elif tier == '3':
                sales_order = SalesOrder(
                    poNumber=po_number,
                    status=self._exporter.erp_config.default_sales_order_status,
                    type=self._exporter.erp_config.default_sales_order_type,
                    customerId=customer.id,
                    billToAddressId=billToAddressId,
                    shipToAddressId=shipToAddressId,
                    terms=payment_details.payment_terms if payment_details.payment_terms is not None else 'Net 30',
                    freightTerms=self._exporter.erp_config.default_sales_order_freight_terms,
                    fob='',
                    poNumberRevision='',
                    note=f'Paperless Parts Quote: https://app.paperlessparts.com/quotes/edit/{quoteNumberWithRevision}',
                )
            else:
                raise NotImplementedError
            if create:
                return sales_order.create()
            else:
                return sales_order

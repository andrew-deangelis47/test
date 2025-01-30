from typing import Optional

from paperless.objects.quotes import Quote

from globalshop.customer import CustomerRecord  # CustomerShipTo
from paperless.objects.orders import OrderItem, Order as PPOrder, Order

from baseintegration.integration import logger
from globalshop.exporter.processors import GSProcessor
from globalshop.order import OrderLine
from globalshop.utils import pad_part_num


class OrderLineProcessor(GSProcessor):

    def _get_customer_part(self, order: Order = None) -> Optional[str]:
        quote, rev = self.get_quote_number(order)
        quote = Quote.get(quote, rev)
        date = quote.sent_date
        logger.debug(f'quote number: {quote.number, rev}')
        customer_part = f'PRICED {date}'
        return customer_part[:17]

    def get_quote_number(self, order):
        if order.quote_revision_number is not None:
            quote = order.quote_number
            rev = order.quote_revision_number
        else:
            quote = order.quote_number
            rev = None
        return quote, rev

    def _process(self, order: PPOrder, order_item: OrderItem,
                 line_number: int, customer_record: CustomerRecord):
        # For each line, insert a record:
        # TODO: Move some of this logic to the Customer/Contact exporter
        #  processors:
        # get the erp_code

        erp_code = None
        account_id = None

        contact = order.contact
        account = contact.account
        if account:
            # account: Account = Account.get(account_id)
            erp_code = account.erp_code
            account_id = account.id
        # sort_code = None
        # use_cust_id_as_sort_code = \
        #     self._exporter.erp_config.use_cust_id_as_sort_code
        # if use_cust_id_as_sort_code:
        #     logger.info(f'Config option "user_cust_id_as_sort_code" is '
        #                 f'True, setting part sort codes to {erp_code}')
        #     # This will be used later in creating the parts
        # self._exporter.erp_config.cust_code = erp_code
        # else:
        #     TODO: Alert that no customer was set?

        # FIXME: The order header info really only needs to be processed
        #  once, then supplied to each subsequent line. Refactor this part!

        root_component = order_item.root_component
        # combine part and revision to ensure 20 character combination
        ext_part_number = pad_part_num(root_component.part_number)
        rev = root_component.revision if root_component.revision else ''
        description = root_component.description
        gss_part_number = f'{ext_part_number}{rev}'

        qty_ordered = order_item.quantity
        line_total_price = order_item.total_price.raw_amount
        line_unit_price = order_item.unit_price.raw_amount

        ship_dates_match = True
        order_item_ships_on = None
        for orderitem in order.order_items:
            if order_item_ships_on is None:
                order_item_ships_on = orderitem.ships_on
            if order_item_ships_on != orderitem.ships_on:
                ship_dates_match = False

        if ship_dates_match:
            order_due_date = order.ships_on[:10]
        else:
            order_due_date = '1900-01-01'
        order_date = order.created[:10]
        line_order_date = order.created[:10]
        line_promise_date = order_item.ships_on

        shipping_info = order.shipping_info

        ship_to_address_1 = shipping_info.address1 if shipping_info else ''
        ship_to_address_2 = shipping_info.address2 if shipping_info else ''
        ship_to_city = shipping_info.city if shipping_info else ''
        ship_to_state = shipping_info.state if shipping_info else ''
        ship_to_zip = shipping_info.postal_code if shipping_info else ''
        ship_to_country = shipping_info.country if shipping_info else ''

        ship_to_contact_name = f"{contact.first_name} {contact.last_name}"
        ship_to_contact_email = contact.email
        #
        # are we getting the ship to address in our sales order

        # ship_id = shipping_info.id
        # ship_to_id = ''
        # if ship_id and ship_to_address_1 != '':
        #     customer_ship_tos = CustomerShipTo.select(customer_id=erp_code)
        #     for customer_ship_to in customer_ship_tos:
        #         if customer_ship_to.address1 == ship_to_address_1:
        #             ship_to_id = customer_ship_to.ship_seq
        #             logger.debug(f'ShipToID: {ship_to_id}')
        #             break

        billing_info = order.billing_info

        bill_to_address_1 = billing_info.address1 if billing_info else ''
        bill_to_address_2 = billing_info.address2 if billing_info else ''
        bill_to_city = billing_info.city if billing_info else ''
        bill_to_state = billing_info.state if billing_info else ''
        bill_to_zip = billing_info.postal_code if billing_info else ''
        bill_to_country = billing_info.country if billing_info else ''

        customer_po = order.payment_details.purchase_order_number if order.payment_details.purchase_order_number else ''
        customer_part = self._get_customer_part(order)
        logger.info(f'Processing Order # {order.number} Line: ')
        OrderLine.insert(gss_customer_no=erp_code,
                         ext_customer_no=str(account_id),
                         line_number=line_number,
                         external_order_no=str(order.number),
                         gss_part_number=gss_part_number,
                         ext_part_number=ext_part_number,
                         qty_ordered=qty_ordered,
                         line_total_price=line_total_price,
                         line_unit_price=line_unit_price,
                         order_due_date=order_due_date,
                         order_date=order_date,
                         line_order_date=line_order_date,
                         line_promise_date=line_promise_date,
                         # ship_to_id=ship_to_id,
                         ship_to_address_1=ship_to_address_1,
                         ship_to_address_2=ship_to_address_2,
                         ship_to_city=ship_to_city,
                         ship_to_state=ship_to_state,
                         ship_to_zip=ship_to_zip,
                         ship_to_country=ship_to_country,
                         ship_to_contact_email=ship_to_contact_email,
                         ship_to_contact_name=ship_to_contact_name,
                         bill_to_address_1=bill_to_address_1,
                         bill_to_address_2=bill_to_address_2,
                         bill_to_city=bill_to_city,
                         bill_to_zip=bill_to_zip,
                         bill_to_state=bill_to_state,
                         bill_to_country=bill_to_country,
                         customer_po=customer_po,
                         part_description=description,
                         customer_part=customer_part
                         )

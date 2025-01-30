from e2.exporter.processors.order_header import OrderHeaderProcessor
from e2.models import Nextnumber, Order
from baseintegration.datamigration import logger


class E2ShopSystemOrderHeaderProcessor(OrderHeaderProcessor):

    def _process(self, order, customer, ship_to, business_name, contact, sales_id):
        quote_no = self.get_quote_number(order)
        customer_description = business_name
        terms_code = self.get_terms_code(order, customer)
        tax_code = self.get_tax_code(customer)
        ship_code = self.get_ship_code(ship_to)
        po_number = self.get_po_number(order)
        purch_contact = self.get_purch_contact(contact)

        currency_code, exchange_rate = self.get_currency_info(order, customer)

        order_total = float(order.payment_details.total_price.dollars)

        date_entered = self.get_date_entered()
        main_due_date = self.get_due_date(order)

        entered_by = self.get_entered_by(order)
        order_no = self.get_order_number()
        logger.info(f"New order no determined by integration is {order_no}")
        order_header = Order(
            order_no=order_no,
            quote_no=quote_no,
            customer_code=customer.customer_code,
            customer_desc=customer_description,
            po_num=po_number,
            date_ent=date_entered,
            ent_by=entered_by,
            sales_id=sales_id,
            terms_code=terms_code,
            tax_code=tax_code,
            purch_contact=purch_contact,
            notes_to_cust='',
            wo_printed='N',
            ack_printed='N',
            jt_printed='N',
            order_total=order_total,
            status='O',
            territory='',  # TODO - How should this work?
            main_due_date=main_due_date,
            main_priority=50,
            gst_code='',
            currency_code=currency_code,
            exch_rate=exchange_rate,
            date_ent_label=date_entered,
            ship_code=ship_code,
            user_date1=None,
            user_date2=None,
            user_text1='',
            user_text2='',
            user_text3='',
            user_text4='',
            user_currency1=None,
            user_currency2=None,
            user_number1=None,
            user_number2=None,
            user_number3=None,
            user_number4=None,
            user_memo1='',
            convert_me=None
        )
        order_header.save()
        order_header: Order = self.update_order_header_shipping_address(order_header, ship_to)
        if not order_header.ship_to_name:
            order_header.ship_to_name = customer_description
            order_header.save()
        self._exporter.success_message = f"Associated E2 order number is {order_no}"
        return order_header

    def get_order_number(self):
        # e2 could potentially overwrite next number so you cannot rely solely on it, must also query the order table
        order_next_num_obj = Nextnumber.objects.filter(object="ORDER").first()
        order_next_num = order_next_num_obj.nextnumber + 1
        order_highest_no = order_next_num
        for obj in Order.objects.order_by('-order_no'):
            try:
                potential_highest_no = int(obj.order_no)
                if potential_highest_no > order_highest_no:
                    order_highest_no = potential_highest_no
                break
            except ValueError:
                continue
        order_next_num_obj.nextnumber = order_highest_no
        order_next_num_obj.save()
        return str(order_highest_no)

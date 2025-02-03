from decimal import Decimal
from datetime import datetime
from baseintegration.utils import trim_django_model

import e2.models as e2
from e2.exporter.processors import E2Processor


class OrderHeaderProcessor(E2Processor):
    do_rollback = False

    def get_quote_number(self, order):
        if order.quote_revision_number is not None:
            quote_number = f'{order.quote_number}-{order.quote_revision_number}PP'
        else:
            quote_number = f'{order.quote_number}PP'
        return quote_number

    def get_terms_code(self, order, customer):
        if order.payment_details.payment_type == 'credit_card':
            terms_code = self._exporter.erp_config.credit_card_terms_code
        else:
            terms_code = customer.termscode
        return terms_code

    def get_tax_code(self, customer):
        return customer.taxcode  # TODO - note, we're not setting this right now upon customer creation

    def get_ship_code(self, ship_to):
        if ship_to is not None and hasattr(ship_to, 'shipcode'):
            return ship_to.shipcode
        else:
            return None

    def get_po_number(self, order):
        return order.payment_details.purchase_order_number

    def get_currency_info(self, order, customer):
        currency_code = customer.currencycode
        exchange_rate = 1.
        return currency_code, exchange_rate

    def get_due_date(self, order):
        due_date = datetime.strptime(order.ships_on, '%Y-%m-%d')
        return due_date

    def get_entered_by(self, order):
        return self._exporter.erp_config.entered_by

    def get_purch_contact(self, contact):
        purch_contact = contact.contact
        return purch_contact

    def update_order_header_shipping_address(self, order_header, ship_to):
        if ship_to is not None:
            order_header.ship_addr1 = ship_to.saddr1
            order_header.ship_addr2 = ship_to.saddr2
            order_header.ship_city = ship_to.scity
            order_header.ship_state = ship_to.sstate
            order_header.ship_zip = ship_to.szipcode
            order_header.phone = ship_to.shipphone
            order_header.fax = ship_to.shipfax
            order_header.country = ship_to.scountry
            if hasattr(ship_to, 'location'):
                order_header.ship_to_name = ship_to.shiptoname
                order_header.ship_via = ship_to.shipvia  # TODO - note, we're not setting this right now from the order
                order_header.location = ship_to.location
            order_header = trim_django_model(order_header)
            order_header.save()
        return order_header

    def _process(self, order, customer, ship_to, business_name, contact, sales_id):
        self.order = order
        quote_no = self.get_quote_number(order)
        customer_description = business_name
        terms_code = self.get_terms_code(order, customer)
        tax_code = self.get_tax_code(customer)
        ship_code = self.get_ship_code(ship_to)
        po_number = self.get_po_number(order)
        purch_contact = self.get_purch_contact(contact)

        currency_code, exchange_rate = self.get_currency_info(order, customer)

        order_total = Decimal(order.payment_details.total_price.dollars)

        date_entered = self.get_date_entered()
        main_due_date = self.get_due_date(order)

        entered_by = self.get_entered_by(order)
        location = self.get_location(order)

        order_header = e2.Order(
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
            location=location,
            convert_me=None,
            last_mod_date=None,
            last_mod_user=None
        )
        order_header = trim_django_model(order_header)
        order_header.save_with_autonumber()
        order_header = self.update_order_header_shipping_address(order_header, ship_to)
        self._exporter.success_message = f"Associated E2 order number is {order_header.order_no}"
        return order_header

    def get_location(self, order):
        return self._exporter.erp_config.default_sales_order_location

    def get_date_entered(self):
        now = datetime.now()
        date_entered = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        return date_entered

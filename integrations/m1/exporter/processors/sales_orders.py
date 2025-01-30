from baseintegration.datamigration import logger
from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order

from m1.constants import DEFAULT_PAYMENT_TERM_MAP
from m1.models import Salesorders, Organizations, Paymentterms
from django.db import connection


class ProcessSalesOrder(BaseProcessor):

    def _process(self, order: Order, org: Organizations):
        if org and org.cmoorganizationid:
            erp_code = org.cmoorganizationid
        else:
            logger.warning(f'Order {order.number}: M1 organization object corrupted.  Bailing...')
            return False

        order_str = 'Paperless Parts Quote #{}\r\n' \
                    'https://app.paperlessparts.com/quotes/edit/{}\r\n' \
                    'Paperless Parts Order #{}\r\n' \
                    'https://app.paperlessparts.com/orders/edit/{}\r\n\r\n'.format(order.quote_number,
                                                                                   order.quote_number,
                                                                                   order.number,
                                                                                   order.number)
        comment = f'{order_str}'

        cursor = connection.cursor()

        try:  # pragma: no cover
            last_sales_order_query = "SELECT TOP 1 Num=CAST(ompSalesOrderID AS int) FROM dbo.SalesOrders ORDER BY Num desc"
            cursor.execute(last_sales_order_query)
            last_sales_order_set = cursor.fetchall()
            last_sales_order_num = last_sales_order_set[0][0]
            new_order_num = f'{int(last_sales_order_num) + 1}'
        except:
            new_order_num = f'pp{order.number}'
            logger.warning(f'Order {order.number}: The next numeric M1 sales order id could not be determined. '
                           f'Using alpha numeric id{new_order_num}')
            cursor.close()
            connection.close()
        finally:
            cursor.close()
            connection.close()

        existing_sales_order: list[Salesorders] = Salesorders.objects.filter(ompsalesorderid=new_order_num)

        customer_po = order.payment_details.purchase_order_number if order.payment_details.purchase_order_number else ''

        pp_term_converted = self.convert_pp_payment_terms(term=order.payment_details.payment_terms)
        payment_term_id = pp_term_converted if pp_term_converted else org.cmocustomerpaymenttermsid

        if len(existing_sales_order) > 0:
            logger.info('Order already exists in M1, bailing out....')
            return False

        new_sales_order = Salesorders.objects.create(ompsalesorderid=new_order_num,
                                                     ompcustomerorganizationid=erp_code,
                                                     omporderdate=order.created_dt,
                                                     omprequestedshipdate=order.ships_on_dt,
                                                     ompordercommentsrtf=comment,
                                                     ompordercommentstext=comment,
                                                     ompcustomerpo=customer_po,
                                                     omppaymenttermid=payment_term_id,
                                                     ompcreatedfromweb=False,
                                                     ompreadytoprint=True,
                                                     ompcustomrate=False,
                                                     ompclosed=False,
                                                     ompdeposit=False,
                                                     ompdepositcreated=False,
                                                     ompavalarataxcalculated=False,
                                                     ompeasyorderenabled=False,
                                                     ompcreatedbyedi=False,
                                                     ompeasyorderpaid=False,
                                                     ompexchangerate=1.000000,
                                                     ompfullordersubtotalbase=order.payment_details.subtotal.raw_amount,
                                                     ompfullordersubtotalforeign=order.payment_details.subtotal.raw_amount,
                                                     ompdiscounttotalbase=0.0000,
                                                     ompdiscounttotalforeign=0.0000,
                                                     ompordersubtotalbase=order.payment_details.subtotal.raw_amount,
                                                     ompordersubtotalforeign=order.payment_details.subtotal.raw_amount,
                                                     ompfreightsubtotalbase=0.0000,
                                                     ompfreightsubtotalforeign=0.0000,
                                                     omptotalorderweight=0.0000,
                                                     ompfreightamountbase=0.0000,
                                                     ompfreightamountforeign=0.0000,
                                                     ompfreighttotalbase=0.0000,
                                                     ompfreighttotalforeign=0.0000,
                                                     ompfreighttaxamountbase=0.0000,
                                                     ompfreighttaxamountforeign=0.0000,
                                                     ompsecondfreighttaxamtbase=0.0000,
                                                     ompsecondfreighttaxamtforeign=0.0000,
                                                     ompordertaxamountbase=0.0000,
                                                     ompordertaxamountforeign=0.0000,
                                                     ompordertotalbase=order.payment_details.total_price.raw_amount,
                                                     ompordertotalforeign=order.payment_details.total_price.raw_amount,
                                                     ompdepositpercent=0.00,
                                                     ompdepositamountbase=0.0000,
                                                     ompdepositamountforeign=0.0000,
                                                     omptaxsubtotalbase=0.0000,
                                                     omptaxsubtotalforeign=0.0000,
                                                     ompsplitpercenttotal=0.00,
                                                     ompstatus=3,
                                                     ompeasyorderstatus=0,
                                                     ompcreatedby='ppadmin',
                                                     ompshiporganizationid=erp_code
                                                     )
        return new_sales_order

    @staticmethod
    def convert_pp_payment_terms(term: str) -> str:
        payment_term_id = None
        term_code = term
        for key, value in DEFAULT_PAYMENT_TERM_MAP.items():
            if value == term_code:
                term_code = key
        m1_terms: Paymentterms = Paymentterms.objects.filter(xatpaymenttermid=term_code)
        if len(m1_terms) > 0:
            payment_term_id = m1_terms[0].xatpaymenttermid
        return payment_term_id

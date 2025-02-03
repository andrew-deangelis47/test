from mietrak_pro.exporter.processors import MietrakProProcessor
from baseintegration.datamigration import logger

from mietrak_pro.query.sales_order import create_sales_order
from paperless.objects.orders import Order
import mietrak_pro.models


class SalesOrderProcessor(MietrakProProcessor):
    do_rollback = False

    def _process(self, order: Order,
                 customer: mietrak_pro.models.Party,
                 contact: mietrak_pro.models.Party,
                 billing_address: mietrak_pro.models.Address,
                 shipping_address: mietrak_pro.models.Address):
        po_number = self.get_po_number(order)
        fob = self.get_fob(order, customer)
        private_notes = self.get_private_notes(order)
        request_for_quote = self.get_request_for_quote(order)
        if request_for_quote is not None:
            request_for_quote_number = request_for_quote.requestforquotenumber
        else:
            request_for_quote_number = None

        division_pk = self._exporter.division_pk
        quote_num_rev = str(order.quote_number)

        if order.quote_revision_number:
            quote_num_rev += f'-{str(order.quote_revision_number)}'

        logger.info('Creating Sales Order')
        sales_order = create_sales_order(customer, contact, billing_address, shipping_address, po_number, fob,
                                         private_notes, request_for_quote_number,
                                         division_pk, order.estimator, quote_num_rev,
                                         self._exporter.erp_config.pp_quote_reference_field)

        # Set the sales order number on the RFQ record, if applicable
        if request_for_quote is not None:
            request_for_quote.salesordernumber = sales_order.salesordernumber
            request_for_quote.save()

        logger.info(f'Sales order created -> {vars(sales_order)}')
        return sales_order

    def get_private_notes(self, order):
        private_notes = order.private_notes
        return private_notes

    def get_po_number(self, order):
        return order.payment_details.purchase_order_number

    def get_fob(self, order, customer):
        return self._exporter.erp_config.default_sales_order_fob

    def get_request_for_quote(self, order: Order):
        if order.quote_erp_code is None:
            return
        try:
            request_for_quote_pk = int(order.quote_erp_code)
            request_for_quote = \
                mietrak_pro.models.Requestforquote.objects.filter(requestforquotepk=request_for_quote_pk).first()
            return request_for_quote
        except:
            return

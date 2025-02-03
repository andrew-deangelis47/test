from typing import Optional

from mietrak_pro.models import Requestforquote, Item
from mietrak_pro.exporter.processors import MietrakProProcessor
from paperless.objects.quotes import QuoteItem
from mietrak_pro.query.request_for_quote import create_request_for_quote_line, create_request_for_quote_line_quantity
import mietrak_pro.models


class RequestForQuoteLineProcessor(MietrakProProcessor):
    do_rollback = False

    def _process(self,
                 request_for_quote: Requestforquote,
                 quote_item: QuoteItem,
                 root_component_part: Item,
                 quote_line_reference_number: int,
                 estimator: Optional[mietrak_pro.models.User]):
        quantity = self.get_quantity(quote_item)
        unit_price = self.get_unit_price(quote_item, quantity)
        total_price = self.get_total_price(quote_item, quantity)

        request_for_quote_line = create_request_for_quote_line(quote_line_reference_number, quantity,
                                                               request_for_quote, root_component_part,
                                                               estimator)
        create_request_for_quote_line_quantity(request_for_quote_line, quantity, unit_price,
                                               total_price, is_first_quantity=True)

        # Update the RFQ total amount incrementally
        request_for_quote.totalamount = request_for_quote.totalamount + total_price
        request_for_quote.totalextendedamount = request_for_quote.totalamount
        request_for_quote.save()

        return request_for_quote_line

    def get_quantity(self, quote_item: QuoteItem):
        return min((q.quantity for q in quote_item.root_component.quantities))

    def get_unit_price(self, quote_item: QuoteItem, quantity: int):
        for q in quote_item.root_component.quantities:
            if q.quantity == quantity:
                return float(q.unit_price.dollars)

    def get_total_price(self, quote_item: QuoteItem, quantity: int):
        for q in quote_item.root_component.quantities:
            if q.quantity == quantity:
                return float(q.total_price.dollars)

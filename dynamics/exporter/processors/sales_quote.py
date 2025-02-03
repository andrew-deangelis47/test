from typing import Optional

from paperless.objects.quotes import Quote, QuoteComponent

from dynamics.utils import DynamicsExportProcessor, get_quantity
from dynamics.objects.customer import Customer, Contact
from dynamics.objects.item import Item
from dynamics.objects.sales_quote import SalesQuote, SalesQuoteLine


class SalesQuoteProcessor(DynamicsExportProcessor):

    def _process(self, quote: Quote, quote_customer: Customer, quote_contact: Optional[Contact]) -> SalesQuote:
        return SalesQuote.create({
            "Sell_to_Customer_No": quote_customer.No,
            "Sell_to_Contact_No": quote_contact and quote_contact.No
            # "Due_Date": quote.deliver_by,  # TODO: add this back once due date is in the Paperless Quote API
            # "External_Document_No": quote.payment_details.purchase_order_number # TODO: same for this
        })


class SalesQuoteLineProcessor(DynamicsExportProcessor):

    def _process(self, parent_quote: SalesQuote, item: Item, component: QuoteComponent) -> SalesQuoteLine:
        return SalesQuoteLine.create({
            "Document_No": parent_quote.No,
            "Type": "Item",
            "No": item.No,
            "Quantity": get_quantity(component)
        })

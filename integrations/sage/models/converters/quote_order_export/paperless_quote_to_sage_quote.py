from sage.models.sage_models import SalesQuote


class PaperlessOrderToSageQuote:
    def create_sales_quote_model(self, sales_quote, quote_line_items) -> SalesQuote:

        sales_site = sales_quote['sales_site']
        reference = sales_quote['reference']
        quote_type = sales_quote['quote_type']
        quote_date = sales_quote['quote_date']
        customer_id = sales_quote['customer_id']
        currency = sales_quote['currency']
        delivery_address = sales_quote['delivery_address']
        shipment_site = sales_quote['shipment_site']

        sage_sales_quote = SalesQuote()

        sage_sales_quote.sales_site = sales_site
        sage_sales_quote.reference = reference
        sage_sales_quote.quote_type = quote_type
        sage_sales_quote.quote_date = str(quote_date)
        sage_sales_quote.customer_id = str(customer_id)
        sage_sales_quote.currency = currency
        sage_sales_quote.delivery_address = delivery_address
        sage_sales_quote.shipment_site = shipment_site
        sage_sales_quote.line_items = quote_line_items

        return sage_sales_quote

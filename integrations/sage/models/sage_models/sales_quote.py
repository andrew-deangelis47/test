

class SalesQuote:

    sales_site: str
    quote_type: str
    reference: str
    quote_date: str
    customer_id: str
    currency: str
    delivery_address: str
    shipment_site: str

    def __init__(self):
        self.sales_site: str = 'ARC01'
        self.quote_type: str = 'SQN'
        self.reference: str = 'TODAY_TEST'
        self.quote_date: str = '20221129'
        self.customer_id: str = 'C00045'
        self.currency: str = 'USD'
        self.delivery_address: str = 'BILL'
        self.shipment_site: str = 'ARC01'

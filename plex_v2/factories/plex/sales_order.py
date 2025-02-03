from plex_v2.objects.sales_orders import SalesOrder
from plex_v2.objects.customer import Customer
from paperless.objects.orders import Order
from paperless.objects.quotes import Quote
from plex_v2.objects.sales_orders import SalesOrder2Tier
from plex_v2.factories.base import BaseFactory
from datetime import datetime
from plex_v2.objects.customers_api_get import CustomersApiGet
from typing import List
from baseintegration.datamigration import logger


class SalesOrderFactory(BaseFactory):

    def to_tier_3_sales_order(self, po_number: str, customer: Customer, billToAddressId: str, shipToAddressId: str, pp_order: Order, quote_no_w_revision: str):

        return SalesOrder(
            poNumber=po_number,
            status=self.config.default_sales_order_status,
            type=self.config.default_sales_order_type,
            customerId=customer.id,
            billToAddressId=billToAddressId,
            shipToAddressId=shipToAddressId,
            terms=self._get_payment_terms(pp_order, customer),
            freightTerms=self.config.default_sales_order_freight_terms,
            fob='',
            poNumberRevision='',
            note=f'Paperless Parts Quote: https://app.paperlessparts.com/quotes/edit/{quote_no_w_revision}',
            orderDate=self._get_order_date()
        )

    def to_tier_2_sales_order(self, po_number: str, customer: Customer, billToAddressId: str, shipToAddressId: str, pp_order: Order, quote_no_w_revision: str):
        quote: Quote = self._get_quote(pp_order)

        return SalesOrder2Tier(
            PO_No=po_number,
            Customer_Code=customer.code,
            customerId=customer.id,
            Bill_To_Customer_Address_Code=billToAddressId,
            Ship_To_Customer_Address_Code=shipToAddressId,
            Inside_Sales=self._get_salesperson(pp_order),
            Note=f'Paperless Parts Quote: https://app.paperlessparts.com/quotes/edit/{quote_no_w_revision} '
                 f'\n {pp_order.private_notes}',
            Printed_Note=quote.quote_notes,
            c_url=self.config.datasources_tier_2_order,
            Ship_From_Building_Code=self.config.default_ship_from_building_code,
            Order_Terms=self._get_payment_terms(pp_order, customer),
            Freight_Terms=self.config.default_sales_order_freight_terms,
            Carrier_Code=self.config.default_sales_order_carrier_code,
            PO_Category=self.config.default_sales_order_category,
        )

    def _get_order_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    def _get_customer_payment_terms(self, customer: Customer):
        customer_information: List[CustomersApiGet] = CustomersApiGet.get(customer.code)
        if len(customer_information) == 0:
            logger.info(
                f'Could not get customer information from plex data source {CustomersApiGet.get_resource_name()}. Customer code is {customer.code}. Will use default payment terms ("{self.config.default_payment_terms}")')

        customer_information: CustomersApiGet = customer_information[0]
        return customer_information.Terms

    def _get_payment_terms(self, pp_order: Order, plex_customer: Customer) -> str:
        # 1) if configured use the Plex customer's payment terms
        if self.config.should_use_customer_terms:
            return self._get_customer_payment_terms(plex_customer)

        # otherwise try to get terms from the payment details on the order, if not use default
        terms = pp_order.payment_details.payment_terms
        if terms is None:
            return self.config.default_sales_order_payment_terms

        return terms

    def _get_quote(self, pp_order: Order) -> Quote:
        return Quote.get(id=pp_order.quote_number, revision=pp_order.quote_revision_number)

    def _get_salesperson(self, pp_order: Order) -> str:
        return f'{pp_order.sales_person.first_name} {pp_order.sales_person.last_name}'.upper()

from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order
from baseintegration.exporter import logger
from epicor.quote import QuoteHeader, QuoteContact
from epicor.customer import Contact
from typing import Optional, Union
from epicor.utils import QuoteHeaderData, CustomerData
from baseintegration.utils import safe_get


class QuoteContactProcessor(BaseProcessor):

    def _process(self, order: Order, customer: CustomerData, quote_header: QuoteHeader,
                 quote_header_data: Optional[QuoteHeaderData] = None):

        if not self._exporter.erp_config.should_add_quote_contacts:
            logger.info("Quote contacts are disabled. Check config.")
            return None

        logger.info(f"Processing quote contact for order: {order.number}")
        quote_contact = self.create_quote_contact(customer, order, quote_header)

        return quote_contact

    def create_quote_contact(self, customer: CustomerData, order: Order, quote_header: QuoteHeader) -> QuoteContact:

        customer_pk, customer_user_num = self.get_customer_code(customer)
        quote_num = quote_header.QuoteNum

        contact_data = customer.contact
        contact_number, contact_id = self.get_contact_number(contact_data)
        contact_name = self.get_contact_name(order, contact_data)
        ship_to_num = self.get_ship_to_num(quote_header)

        quote_contact = None
        if contact_number is not None and contact_id is not None:
            try:
                quote_contact = QuoteContact(
                    Company=str(self._exporter.erp_config.company_name),
                    QuoteNum=int(quote_num),
                    CustNum=customer_pk,
                    ShipToNum=ship_to_num,
                    ConNum=contact_number,
                    PerConID=contact_id,
                    Name=contact_name,
                    CustNumCustID=customer_user_num,
                ).create_instance()
                logger.info(f"Created quote contact: {customer.contact} for quote: {quote_num}")
            except Exception as e:
                logger.info(f"Could not create quote contact: {e}")

        return quote_contact

    def get_customer_code(self, cust: CustomerData) -> tuple:
        customer_pk = int(cust.customer.CustNum)  # Customer PK ID
        customer_user_num = str(cust.customer.CustID)  # User-defined customer number
        return customer_pk, customer_user_num

    def get_contact_number(self, contact: Union[Contact, None]) -> Union[tuple, None]:
        """
        - Gets contact number from the Epicor Contact object assigned to the CustomerData object in customer.py
        """
        if not contact:
            logger.info("No Contact exists for this. Cannot create quote contact.")
            return None, None

        contact_number = safe_get(contact, "ConNum", None)
        per_con_id = safe_get(contact, "PerConID", None)
        if contact_number and per_con_id:
            return int(contact_number), int(per_con_id)
        return None, None

    def get_contact_name(self, order: Order, contact: Union[Contact, None]) -> Union[str, None]:
        """
        - Attempts to get contact name from Epicor Contact object assigned to the CustomerData object in customer.py
        - Else, gets contact name from the Paperless order contact information
        """
        if contact:
            return safe_get(contact, "Name", None)
        elif order and order.contact:
            return f"{order.contact.first_name} {order.contact.last_name}"
        return None

    def get_ship_to_num(self, quote_header: QuoteHeader):
        return safe_get(quote_header, "ShipToNum", None)

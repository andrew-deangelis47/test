from paperless.objects.orders import Order
from baseintegration.utils import logger
from epicor.quote import QuoteHeader
from epicor.customer import Customer
from epicor.utils import QuoteHeaderData
from typing import Optional, Union
from epicor.utils import CustomerData
from paperless.objects.users import User
from epicor.salesperson import Salesperson
from epicor.exporter.v2_processors.base import EpicorProcessor


class QuoteHeaderProcessor(EpicorProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'quote_header'

    def _process(self, order: Order, customer_data: CustomerData,
                 quote_header_data: Optional[QuoteHeaderData]) -> QuoteHeader:

        try:
            logger.info("Instantiated process method on the QuoteHeaderProcessor")
            customer: Customer = customer_data.customer

            customer_id = self.get_customer_id(customer)
            customer_number = self.get_customer_number(customer)
            customer_terms_code = self.get_customer_default_terms_code(customer)
            quoted_status = self.get_quoted_status()
            ship_to_num = self._get_ship_to_num(customer_data)
            contact_num = self._get_contact_num(customer_data)
            quote_comment = self._get_quote_commends(order)
            purchase_order_number = self.get_purchase_order_number(order)
            need_by_date = self.get_due_date(order)
            quote_created_on_date = self.get_quote_created_on_date(order)
            sales_rep = self._get_sales_rep_code(order)
            reference = self._get_quote_num_reference_value(order)

            # TODO: Sales reps must be matched with a salesperson object in Epicor - needs more discovery
            # sales_rep_name = self.get_sales_person(order)
            logger.info("Attempting to create Epicor Quote Header")

            quote_header = QuoteHeader(
                CustNum=customer_id,  # Customer PK ID
                CustomerCustID=str(customer_number),  # User-defined customer number
                TermsCode=customer_terms_code,
                Quoted=quoted_status,
                ShipToNum=ship_to_num,
                ShipToCustNum=customer_id,
                ShpConNum=contact_num,
                QuoteComment=quote_comment,
                PONum=purchase_order_number,
                SalesRepCode=sales_rep,
                DueDate=need_by_date,
                NeedByDate=need_by_date,
                EntryDate=quote_created_on_date,
                Reference=reference,
            ).create_instance()

        except Exception as e:
            logger.info(f'Unexpected exception: {e}')
            self._add_report_message('Unexpected error when creating the quote header. Please contact support.')
            raise e

        logger.info(f"Created quote header: {quote_header}")
        self._exporter.success_message = f"Associated Epicor quote number is {quote_header.QuoteNum}"
        self._add_report_message(f'Created Epicor quote header number {quote_header.QuoteNum}')
        return quote_header

    def get_quote_created_on_date(self, order: Order) -> Union[str, None]:
        quote_created_on_date = order.created
        return str(quote_created_on_date)

    def get_sales_person(self, order: Order) -> Union[str, None]:
        sales_person_dict = order.sales_person
        if sales_person_dict.first_name and sales_person_dict.last_name:
            return f"{sales_person_dict.first_name} {sales_person_dict.last_name}"
        return None

    def get_due_date(self, order: Order) -> Union[str, None]:
        ship_date = order.ships_on
        return str(ship_date)

    def get_purchase_order_number(self, order: Order) -> Union[str, None]:
        po_number = order.payment_details.purchase_order_number
        if po_number is not None:
            return str(po_number)
        return None

    def get_customer_id(self, customer: Customer) -> int:
        customer_id = int(customer.CustNum)  # Customer PK ID
        return customer_id

    def get_customer_number(self, customer: Customer) -> str:
        customer_number = str(customer.CustID)  # User-defined customer number
        return customer_number

    def get_customer_default_terms_code(self, customer: Customer):
        return str(customer.TermsCode)

    def get_quoted_status(self) -> bool:
        """
        This function exists as a placeholder for potential future customizations.
        """
        return self._exporter.erp_config.should_mark_quotes_as_quoted

    def _get_ship_to_num(self, customer_data: CustomerData) -> Union[str, None]:
        if customer_data.shipping_address is not None:
            ship_to_num = str(customer_data.shipping_address.ShipToNum)
            return ship_to_num
        return None

    def _get_contact_num(self, customer_data: CustomerData) -> Union[int, None]:
        if customer_data.contact is not None:
            contact_num = customer_data.contact.ConNum
            if contact_num is not None:
                return contact_num
        return None

    def _get_quote_commends(self, order: Order) -> str:
        quote_num = order.quote_number
        quote_rev = order.quote_revision_number
        if quote_num and quote_rev:
            quote_num = f"{quote_num}-{quote_rev}"
        notes = f"This quote originated from Paperless Parts order number: {order.number}\n" \
                f"Original Paperless Parts quote number: {quote_num}" \
                f"View original quote: 'https://app.paperlessparts.com/orders/edit/{order.number}'\n"
        return notes

    def _get_sales_rep_code(self, order: Order) -> Union[str, None]:
        """
        Placeholder function for mapping Paperless Parts salesperson to Epicor Sales Rep Code
        """
        logger.info("Attempting to get a valid sales rep code from the Paperless salesperson.")
        pp_salesperson_list = User.list()
        pp_salesperson = order.sales_person if order.sales_person is not None else order.salesperson
        pp_salesperson_email = None
        if pp_salesperson is not None:
            pp_salesperson_email = pp_salesperson.email
        sales_rep_code = str(self._exporter.erp_config.default_salesperson_id)

        for user in pp_salesperson_list:
            if user.email == pp_salesperson_email:
                sales_rep_code_is_valid = self._validate_sales_rep_code(user.erp_code)
                sales_rep_code = user.erp_code if sales_rep_code_is_valid else sales_rep_code

        if str(sales_rep_code) == str(self._exporter.erp_config.default_salesperson_id):
            logger.info(f"Returning default sales rep code of {str(sales_rep_code)}")

        return str(sales_rep_code)

    def _validate_sales_rep_code(self, sales_rep_code: str) -> bool:
        try:
            epicor_salesperson = Salesperson.get_by_id(sales_rep_code)
            logger.info(f"Found valid salesperson ID: {epicor_salesperson.SalesRepCode}")
            return True
        except Exception as e:
            logger.info(f"Sales rep code is not valid. {e}")
            return False

    def _get_quote_num_reference_value(self, order: Order) -> Union[str, None]:
        if self._exporter.erp_config.should_populate_reference_with_pp_quote_num:
            if order.quote_revision_number is None:
                quote_number = str(order.quote_number)
            else:
                quote_number = f"{order.quote_number}-{order.quote_revision_number}"
            logger.info(f"Adding Paperless Parts quote number {quote_number} to Epicor reference field.")
            return f"PP#{quote_number}"
        else:
            return None

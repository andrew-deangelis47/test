from typing import Optional

from paperless.exceptions import PaperlessNotFoundException
from paperless.objects.orders import OrderContact
from paperless.objects.customers import Account
from paperless.objects.address import AddressInfo

from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from baseintegration.exporter import logger
from baseintegration.utils import update_account_erp_code
from paperless.objects.customers import PaymentTerms as PaperlessPaymentTerms
from epicor.customer import Customer, PaymentTerms, Contact, ShipTo, Country
from epicor.exceptions import EpicorNotFoundException
from epicor.utils import CustomerData
from epicor.exporter.v2_processors.base import EpicorProcessor


class CustomerProcessor(EpicorProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'customer'

    def _process(self, order_contact: OrderContact, shipping_address: Optional[AddressInfo]) -> CustomerData:
        """
        Process a customer from PaperlessParts into Epicor. Checks to see if
        the customer exists, otherwise creates the customer from the quote &
        address data.
        """

        paperless_account = self._get_paperless_account(order_contact)
        epicor_customer = self._process_customer(paperless_account, order_contact)
        if shipping_address:
            epicor_shipping_address = self._process_shipping_address(shipping_address, epicor_customer)
        else:
            logger.info("No shipping information supplied on the Paperless Parts order facilitation.")
            epicor_shipping_address = None
        epicor_contact = self._process_contact(epicor_customer, order_contact)

        return CustomerData(epicor_customer, epicor_contact, epicor_shipping_address)

    def _get_paperless_account(self, order_contact: OrderContact) -> Account:
        if order_contact.account and order_contact.account.id:
            try:
                return Account.get(order_contact.account.id)
            except PaperlessNotFoundException:
                error_message = f'Paperless Parts Account does not exist for contact: '\
                                f'"{order_contact.first_name} {order_contact.last_name}". '\
                                f'Missing Account name: "{order_contact.account.name}"; '\
                                f'ERP Code: "{order_contact.account.erp_code}"'
                self._add_report_message(error_message)
                raise CancelledIntegrationActionException(error_message)
        else:
            error_message = f'Order contact {order_contact.email} '\
                            f'does not have associated Paperless Parts Account.'
            self._add_report_message(error_message)
            raise CancelledIntegrationActionException(error_message)

    def _process_customer(self, paperless_account: Account, order_contact: OrderContact) -> Customer:
        try:
            epicor_customer: Customer = self._get_customer(paperless_account)
            logger.info('Customer was found')
            self._add_report_message(f'Epicor customer was found. Name is {epicor_customer.Name}')
            return epicor_customer
        except EpicorNotFoundException:
            logger.info('Customer was not found')
            self._add_report_message('Customer was found')
            default_customer_id = self._exporter.erp_config.default_customer_id
            if self._exporter.erp_config.should_create_customer:
                logger.info('Creating customer')
                self._add_report_message(f'Creating customer with default id: {default_customer_id}')
                return self._create_customer(paperless_account, order_contact)
            elif default_customer_id:
                logger.info('Using default customer')
                self._add_report_message('Using default customer.')
                try:
                    return Customer.get_by_id(default_customer_id)
                except EpicorNotFoundException:
                    self._add_report_message(f'Default customer {default_customer_id} not found. Cancelling export.')
                    raise CancelledIntegrationActionException(f'Default customer {default_customer_id} not found')
            else:
                self._add_report_message(f'Cancelled order. Customer: "{paperless_account.name}" does '
                                         f'not exist in Epicor. Create the Epicor customer first '
                                         f'before reprocessing this order. NOTE: The Epicor Customer'
                                         f'ID must match the Paperless Parts ERP Code field.')
                raise CancelledIntegrationActionException(f'Cancelled order. Customer: "{paperless_account.name}" does '
                                                          f'not exist in Epicor. Create the Epicor customer first '
                                                          f'before reprocessing this order. NOTE: The Epicor Customer'
                                                          f'ID must match the Paperless Parts ERP Code field.')

    def _get_customer(self, paperless_account: Account) -> Optional[Customer]:
        """
        - We cannot 'GET' customers by name - name is not a unique field in Epicor.
        - We run the risk of creating duplicate data because of typos, ie. "Company 1" vs. "Company1"
        - We then write back the ERP code on the Paperless created customer.
        - We then forever match with the wrong Epicor customer until the ERP code is corrected.
        """
        logger.info(f'Attempting to match account with ID {paperless_account.erp_code}')
        return Customer.get_by_id(paperless_account.erp_code)

    def _create_customer(self, paperless_account: Account, quote_contact: OrderContact) -> Customer:
        logger.info('Did not find Epicor Company. Creating one!')
        customer_type = self._exporter.erp_config.new_customer_type
        check_duplicate_po = \
            self._exporter.erp_config.new_customer_check_duplicate_po
        sold_to = paperless_account.sold_to_address
        erp_code = self._get_erp_code(paperless_account)
        payment_terms_code = self._get_paperless_payment_terms(paperless_account)

        data = {
            "Company": self._exporter.erp_config.company_name,
            "CustID": erp_code,
            "Name": paperless_account.name,
            "EMailAddress": quote_contact.email,
            "PhoneNum": paperless_account.phone or None,
            "CustomerType": customer_type,
            "CheckDuplicatePO": check_duplicate_po,
            "Comment": paperless_account.notes,
            "CustURL": paperless_account.url,
            "TermsCode": payment_terms_code
        }

        if sold_to:
            data.update({
                "Address1": sold_to.address1,
                "Address2": sold_to.address2,
                "City": sold_to.city,
                "State": sold_to.state,
                "Zip": sold_to.postal_code,
                "Country": sold_to.country
            })

        epicor_company: Customer = Customer.create(data)
        logger.info(f'Created Epicor Company: {epicor_company}')
        self._add_report_message(f'Created Epicor Company: {epicor_company}')

        self._update_pp_erp_code(paperless_account, erp_code)

        return epicor_company

    def _get_paperless_payment_terms(self, paperless_account: Account):
        paperless_payment_terms = PaperlessPaymentTerms.list()
        if paperless_payment_terms:
            for paperless_term in paperless_payment_terms:
                if paperless_account.payment_terms == paperless_term.label and paperless_term.erp_code is not None:
                    logger.info(f"Got Epicor TermsCode from Paperless Parts payment terms object: "
                                f"{paperless_term.erp_code}")
                    return paperless_term.erp_code
        try:
            assert paperless_account.payment_terms
            payment_terms_code = PaymentTerms.get_code_by_description(paperless_account.payment_terms).TermsCode
            logger.info('Got Epicor TermsCode from matched Epicor payment terms description')
        except Exception as e:
            logger.info(f'Payment terms code not found, setting to default. ERROR: {e}')
            payment_terms_code = str(self._exporter.erp_config.default_payment_terms_code)

        return payment_terms_code

    def _process_shipping_address(self, shipping_address: AddressInfo, epicor_customer: Customer) -> Optional[ShipTo]:
        try:
            address = ShipTo.get_first({
                'CustNum': epicor_customer.CustNum,
                'Address1': shipping_address.address1,
                'Address2': shipping_address.address2,
                'City': shipping_address.city,
                'State': shipping_address.state,
                'ZIP': shipping_address.postal_code,
                'Country': shipping_address.country
            })
            logger.info('Shipping address was found')
            return address
        except EpicorNotFoundException:
            logger.info('Shipping address was not found')
            if self._exporter.erp_config.should_create_shipping_address:
                logger.info('Creating shipping address')
                return self._create_shipping_address(shipping_address, epicor_customer)
            else:
                logger.warning('Skipping the creation of shipping address')

    def _create_shipping_address(self, address: AddressInfo, customer: Customer) -> Optional[ShipTo]:
        # get the country number
        country_num: int
        try:
            country_num = Country.get_by('Description', address.country).CountryNum
        except EpicorNotFoundException:
            logger.warning(f'Could not find Epicor country with description {address.country}, skipping address')
            return

        return ShipTo.create({
            "Company": self._exporter.erp_config.company_name,
            "CustNum": customer.CustNum,
            "Name": address.facility_name,
            "ShipToNum": str(address.id),
            "Address1": address.address1,
            "Address2": address.address2 or None,
            "City": address.city,
            "State": address.state,
            "ZIP": address.postal_code,
            "CountryNum": country_num
        })

    def _process_contact(self, epicor_customer: Customer, order_contact: OrderContact) -> Contact:
        logger.info(f'Processing Paperless Contact: {order_contact}')

        try:
            contact = Contact.get_by_cust_and_email(order_contact.email, epicor_customer.CustNum)
            logger.info('Contact was found')
            self._add_report_message(f'Epicor contact was found by matching on email. Name is {contact.Name}.')
            return contact
        except EpicorNotFoundException:
            logger.info('Contact was not found by matching on email. Attempting to get contact by name.')
            self._add_report_message(f'Epicor contact not found via customer id "{epicor_customer.CustNum}". Attempting to match by name.')

        try:
            contact = Contact.get_by_cust_name(order_contact.first_name, order_contact.last_name, epicor_customer.CustNum)
            logger.info('Contact was found')
            self._add_report_message(f'Contact was found by matching on name. Name is {contact.Name}.')
            return contact
        except EpicorNotFoundException:
            logger.info('Contact was still not found.')
            self._add_report_message('Contact still not found.')
            default_contact_email = self._exporter.erp_config.default_contact_email
            if self._exporter.erp_config.should_create_contact:
                logger.info('Creating contact')
                contact: Contact = self._create_contact(epicor_customer, order_contact)
                self._add_report_message(f'Created contact with name {contact.Name}.')
                return contact
            elif default_contact_email:
                logger.info('Using default contact')
                try:
                    contact: Contact = Contact.get_by_cust_and_email(default_contact_email, epicor_customer.CustNum)
                    self._add_report_message(f'Using default contact with name {contact.Name}')
                    return contact
                except EpicorNotFoundException:
                    logger.warning('The default contact could not be found on the customer. Skipping the creation of contact')
                    self._add_report_message('The default contact could not be found on the customer. Skipping the creation of contact')
            else:
                logger.warning('No default contact is configured. Skipping the creation of contact')
                self._add_report_message('No default contact is configured. Skipping the creation of contact.')

    def _create_contact(self, customer: Customer, quote_contact: OrderContact) -> Contact:
        new_contact = None
        try:
            new_contact = Contact.create({
                "Company": self._exporter.erp_config.company_name,
                "CustNum": customer.CustNum,
                "EMailAddress": quote_contact.email,
                "Name": f'{quote_contact.first_name} {quote_contact.last_name}',
                "FirstName": quote_contact.first_name,
                "LastName": quote_contact.last_name,
                "Comment": quote_contact.notes,
                "PhoneNum": quote_contact.phone
            })
        except Exception as e:
            logger.info(f"New contact could not be created. ERROR: {e}")
        return new_contact

    def _get_erp_code(self, paperless_account: Account) -> str:
        erp_code = paperless_account.erp_code[:10] if paperless_account.erp_code is not None else None

        if erp_code is not None:
            return erp_code

        erp_code = self.format_erp_code(paperless_account.name)
        n = 0
        created_new_erp_code: bool = False
        while n <= 99 and created_new_erp_code is False:
            n += 1
            if n < 10:
                erp_code = str(erp_code[:-1]) + str(n)
            if n >= 10 and len(erp_code) >= 2:
                erp_code = str(erp_code[:-2]) + str(n)
            created_new_erp_code = self._create_new_erp_code(erp_code)

        logger.info(f"Identified new ERP Code/CustID: {erp_code}")
        update_account_erp_code(self._exporter._integration, paperless_account.id, erp_code)
        return erp_code

    def format_erp_code(self, erp_code: str) -> str:
        erp_code = erp_code.replace("'", "")
        return erp_code[:10]

    def _create_new_erp_code(self, new_erp_code: str) -> bool:
        logger.info(f'Checking if new ERP code/CustID will create a conflict: {new_erp_code}')
        try:
            Customer.get_by_id(new_erp_code)
            return False
        except EpicorNotFoundException:
            return True

    def _update_pp_erp_code(self, paperless_account: Account, erp_code: str):
        try:
            paperless_account.erp_code = erp_code
            paperless_account.update()
        except Exception as e:
            logger.info(f"Could not update Paperless Parts ERP Code. ERROR: {e}")

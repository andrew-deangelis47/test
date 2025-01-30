from paperless.objects.customers import Account, Contact
from inforvisual.exporter.utils import CustomerData
from baseintegration.exporter import BaseProcessor, logger
from inforvisual.models import Customer
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
import datetime


class CustomerProcessor(BaseProcessor):

    def _process(self, business_name: str, code: str, account_id: int, payment_terms: str, payment_terms_period: int, contact_id: int, billing_info, order_num: int) -> CustomerData:
        # Get or create customer
        customer_is_new = False
        logger.info(f"Getting customer with code {code}")
        customer: Customer = self.get_customer(business_name, code)
        if customer:
            logger.info("Customer was found")
            customer_data = CustomerData(customer=customer, customer_is_new=customer_is_new)
            if self._exporter.erp_config.update_customers:
                logger.info("Update customers is set to true. Updating customer with miscellaneous data")
                self.populate_miscellaneous_customer_data(account_id, customer, payment_terms, payment_terms_period, contact_id, billing_info)
        else:
            if self._exporter.erp_config.update_customers:
                logger.info(f"Update customers is set to true. Creating customer with business name {business_name}")
                customer_data = self.create_customer(business_name, code)
                self.populate_miscellaneous_customer_data(account_id, customer_data.customer, payment_terms,
                                                          payment_terms_period, contact_id, billing_info)
            else:
                if self._exporter.erp_config.send_email_when_customer_not_found:
                    logger.info("Updat customers is set to false and customer was not found. Sending email")
                    self.send_email_notification(business_name)
                raise CancelledIntegrationActionException(f"Customer {business_name} with code {str(code)} not found. We're not bringing it over")
        return customer_data

    def populate_billing_info(self, customer: Customer, billing_info):
        logger.info("Populating billing info on customer")
        if billing_info:
            customer.addr_1 = billing_info.address1
            customer.addr_2 = billing_info.address2
            customer.city = billing_info.city
            customer.state = billing_info.state
            customer.zipcode = billing_info.postal_code
            customer.country = billing_info.country
            customer.bill_to_name = billing_info.business_name
            customer.bill_to_addr_1 = billing_info.address1
            customer.bill_to_addr_2 = billing_info.address2
            customer.bill_to_city = billing_info.city
            customer.bill_to_state = billing_info.state
            customer.bill_to_country = billing_info.country
            customer.bill_to_zipcode = billing_info.postal_code

    def populate_contact_info(self, customer: Customer, contact: Contact):
        logger.info("Populating contact info on customer")
        if contact:
            customer.contact_first_name = contact.first_name
            customer.contact_last_name = contact.last_name
            customer.contact_phone = contact.phone
            customer.contact_email = contact.email

    def populate_miscellaneous_customer_data(self, account_id, customer: Customer, payment_terms, payment_terms_period, contact_id: int, billing_info):
        # Not all of the information we need to instantiate a customer in E2 is present in the OrderAccount object
        # Pull down the full Account object by ID to get the rest of the information we need
        account = Account.get(account_id)
        contact = Contact.get(contact_id)

        logger.info("Checking contact info")
        self.populate_contact_info(customer, contact)
        customer.terms_description = payment_terms
        customer.terms_net_days = payment_terms_period
        customer.tax_exempt = account.tax_exempt

        logger.info("Checking billing info")
        self.populate_billing_info(customer, billing_info)
        customer.save()

    def send_email_notification(self, business_name: str):
        subject = "Order placed in Paperless Parts with new customer"
        body = f'The new customer {business_name} has placed an order which has not been brought into Infor Visual. Please update the ERP system accordingly.'
        self._exporter.send_email(subject, body)

    def get_customer(self, business_name: str, code: str):
        customer = None
        if code is not None:
            logger.info(f"Code {code} exists, checking to see if we have a customer already")
            customer = Customer.objects.filter(id=code).first()
        if not customer:
            logger.info(f"Trying customer lookup via name now for {business_name}")
            customer = Customer.objects.filter(name=business_name).first()
        return customer

    def create_customer(self, business_name: str, code: str):
        if code is None:
            logger.info(f'No CustomerCode record found with id {code}. Creating one')
            code = business_name[0:4].upper() + "01"
        customer = Customer.objects.create(id=code,
                                           name=business_name,
                                           status_eff_date=datetime.datetime.now())
        customer.name = business_name
        customer.save()
        return CustomerData(customer, True)

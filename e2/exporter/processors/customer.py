from e2.query.customer_code import create_customer_code, get_or_create_terms
from e2.query.address import update_billing_address
from paperless.objects.customers import Account
import e2.models as e2
from baseintegration.utils import create_new_paperless_parts_account, update_account_erp_code
from e2.utils.utils import create_addr_dict, CustomerData
from . import E2Processor
from baseintegration.datamigration import logger


class CustomerProcessor(E2Processor):
    # We don't want to rollback customer records on errors
    do_rollback = False

    def update_billing_address(self, customer, billing_info):
        logger.info('Updating customer billing address')
        billing_addr_dict = self.create_billing_addr_dict(billing_info)
        update_billing_address(customer, billing_addr_dict)

    def create_billing_addr_dict(self, billing_info):
        return create_addr_dict(billing_info)

    def update_payment_terms(self, customer, payment_terms, payment_terms_period):
        if payment_terms is not None:
            logger.info(f'Setting payment terms to {payment_terms} with period {payment_terms_period}')
            terms = get_or_create_terms(payment_terms, payment_terms_period)
            customer.termscode = terms.termscode
            customer.save()

    def update_customer_notes(self, customer, customer_notes):
        if customer_notes is not None:
            logger.info('Updating customer notes')
            customer.comments2 = customer_notes
            customer.save()

    def update_customer_sales_id(self, customer, sales_id):
        if sales_id is not None:
            logger.info(f'Updating customer Sales ID to {sales_id}')
            customer.salesid = sales_id
            customer.save()

    def populate_miscellaneous_customer_data(self, account_id, customer, customer_is_new):
        if not customer_is_new:
            return

        if account_id is not None:
            # Not all of the information we need to instantiate a customer in E2 is present in the OrderAccount object
            # Pull down the full Account object by ID to get the rest of the information we need
            account = Account.get(account_id)

            customer.phone = self.get_customer_phone(account)
            customer.defpriority = self.get_priority(account)
            customer.website = self.get_customer_url(account)
            customer.currencycode = self.get_currency_code(account)

        customer.qbcustcode = self.get_quickbooks_customer_code(customer)
        customer.save()

    def get_quickbooks_customer_code(self, customer):
        return customer.customer_code

    def get_currency_code(self, account):
        return self._exporter.erp_config.default_customer_currency_code

    def get_customer_url(self, account):
        return account.url

    def get_customer_phone(self, account):
        return account.phone

    def get_priority(self, account):
        priority = 50
        return priority

    def _process(self, business_name, code, payment_terms, payment_terms_period, customer_notes, order, account_id,
                 contact_id, sales_id):
        # Get or create customer
        customer, customer_is_new, account_id = self.get_or_create_customer(account_id, business_name, code, contact_id)

        self.populate_miscellaneous_customer_data(account_id, customer, customer_is_new)

        # If desired, update the billing address on the CustomerCode to reflect the billing address from the order
        should_update_billing_address = self.should_update_e2_billing_address(customer_is_new)
        if should_update_billing_address:
            billing_info = order.billing_info
            if billing_info is not None:
                self.update_billing_address(customer, billing_info)

        # If desired, update the payment terms on the CustomerCode to reflect the payment terms for the Account,
        # creating a new payment terms record in E2 if necessary
        should_update_payment_terms = self.should_update_e2_payment_terms(customer_is_new)
        if should_update_payment_terms:
            self.update_payment_terms(customer, payment_terms, payment_terms_period)

        # If desired, update the internal customer notes (comments2) on the CustomerCode
        should_update_customer_notes = self.should_update_e2_customer_notes(customer_is_new)
        if should_update_customer_notes:
            self.update_customer_notes(customer, customer_notes)

        # If desired, update the Sales ID on the CustomerCode
        should_update_customer_sales_id = self.should_update_e2_customer_sales_id(customer_is_new)
        if should_update_customer_sales_id:
            self.update_customer_sales_id(customer, sales_id)

        customer_data = CustomerData(customer=customer, customer_is_new=customer_is_new)
        return customer_data

    def should_update_e2_customer_sales_id(self, customer_is_new):
        should_update_customer_sales_id = customer_is_new or self._exporter.erp_config.should_update_e2_customer_sales_id
        return should_update_customer_sales_id

    def should_update_e2_customer_notes(self, customer_is_new):
        should_update_customer_notes = customer_is_new or self._exporter.erp_config.should_update_e2_customer_notes
        return should_update_customer_notes

    def should_update_e2_payment_terms(self, customer_is_new):
        should_update_payment_terms = customer_is_new or self._exporter.erp_config.should_update_e2_payment_terms
        return should_update_payment_terms

    def should_update_e2_billing_address(self, customer_is_new):
        should_update_billing_address = customer_is_new or self._exporter.erp_config.should_update_e2_billing_address
        return should_update_billing_address

    def get_or_create_customer(self, account_id, business_name, code, contact_id):
        customer = None
        customer_is_new = False
        if code is not None:
            customer = e2.CustomerCode.objects.filter(customer_code=code).first()
        if customer is None:
            logger.info(f'No CustomerCode record found with customer_code {code}. Creating one')
            customer: e2.CustomerCode = create_customer_code(business_name)
            customer_is_new = True
            new_erp_code = customer.customer_code
            logger.info(f'Created new CustomerCode record with customer_code {new_erp_code}')
            if account_id is None:
                account_id = create_new_paperless_parts_account(self._exporter._integration, new_erp_code,
                                                                business_name, contact_id)
            elif code is None:
                # If this is a new customer, the existing ERP Code in Paperless Parts should be None
                # Set the ERP Code to the ID that was generated for this newly created customer
                update_account_erp_code(self._exporter._integration, account_id, new_erp_code)
            else:
                pass
        return customer, customer_is_new, account_id

from typing import Optional

from mietrak_pro.query.customer import create_customer, get_or_create_terms
from paperless.objects.customers import Account, AccountList
from mietrak_pro.models import Party

from mietrak_pro.exporter.utils import CustomerData
from mietrak_pro.exporter.processors import MietrakProProcessor
from baseintegration.datamigration import logger
from baseintegration.utils import safe_get, update_account_erp_code, create_new_paperless_parts_account
from mietrak_pro.settings import IS_TEST


class CustomerProcessor(MietrakProProcessor):
    # We don't want to rollback customer records on errors
    do_rollback = False

    def get_payment_terms(self, account: Optional[Account]):
        payment_terms = None
        payment_terms_period = None
        if account is not None:
            payment_terms = account.payment_terms
            payment_terms_period = account.payment_terms_period
        else:
            payment_terms = self._exporter.erp_config.default_terms
            payment_terms_period = self._exporter.erp_config.default_terms_period
        return payment_terms, payment_terms_period

    def update_payment_terms(self, customer: Party, payment_terms: str, payment_terms_period: int):
        if payment_terms is not None:
            logger.info(f'Setting payment terms to {payment_terms} with period {payment_terms_period}')
            terms = get_or_create_terms(payment_terms, payment_terms_period)
            customer.termfk = terms
            customer.save()

    def update_customer_notes(self, customer: Party, customer_notes: Optional[str]):
        if customer_notes is not None:
            logger.info('Updating customer notes')
            customer.notes = customer_notes
            customer.save()

    def update_miscellaneous_customer_data(self, account: Optional[Account], customer: Party, is_customer_new: bool):
        customer.phone = self.get_customer_phone(account)
        customer.website = self.get_customer_url(account)
        customer.save()

    def get_customer_url(self, account: Optional[Account]):
        return safe_get(account, 'url')

    def get_customer_phone(self, account: Optional[Account]):
        if account is None:
            return None
        if account.phone_ext:
            phone_with_ext = f'{account.phone} x{account.phone_ext}'
        else:
            phone_with_ext = account.phone
        return phone_with_ext

    def _process(self, business_name: str, code: int, customer_notes: str, account: Optional[Account], contact_id: int):

        payment_terms, payment_terms_period = self.get_payment_terms(account)

        # Get or create customer
        customer, is_customer_new = self.get_or_create_customer(account, business_name, code, contact_id)
        if is_customer_new and self._exporter.erp_config.should_send_email_when_new_customer_is_created:
            self.send_email_notification(business_name, account)

        # If desired, update the payment terms on the customer to reflect the payment terms for the Account,
        # creating a new payment terms record in MIE Trak Pro if necessary
        should_update_payment_terms = self.should_update_mietrak_pro_payment_terms(is_customer_new)
        if should_update_payment_terms:
            self.update_payment_terms(customer, payment_terms, payment_terms_period)

        # If desired, update the internal customer notes
        should_update_customer_notes = self.should_update_mietrak_pro_customer_notes(is_customer_new)
        if should_update_customer_notes:
            self.update_customer_notes(customer, customer_notes)

        # If desired, update the miscellaneous data for the customer
        should_update_customer_misc_data = self.should_update_mietrak_pro_customer_misc_data(is_customer_new)
        if should_update_customer_misc_data:
            self.update_miscellaneous_customer_data(account, customer, is_customer_new)

        customer_data = CustomerData(customer=customer, is_customer_new=is_customer_new)
        return customer_data

    def send_email_notification(self, business_name: str, account: Optional[Account]):
        subject = f'Paperless Parts Integration has created a new customer in MIE Trak Pro: {business_name}'
        body = f'An order has been placed for new customer {business_name}. A new customer record has been created in ' \
               f'MIE Trak Pro. Please review this customer record.'
        self._exporter.send_email(subject, body)

    def should_update_mietrak_pro_customer_notes(self, is_customer_new: bool):
        should_update_customer_notes = \
            is_customer_new or self._exporter.erp_config.should_update_mietrak_pro_customer_notes
        return should_update_customer_notes

    def should_update_mietrak_pro_payment_terms(self, is_customer_new: bool):
        should_update_payment_terms = \
            is_customer_new or self._exporter.erp_config.should_update_mietrak_pro_payment_terms
        return should_update_payment_terms

    def should_update_mietrak_pro_customer_misc_data(self, is_customer_new: bool):
        should_update_customer_misc_data = \
            is_customer_new or self._exporter.erp_config.should_update_mietrak_pro_customer_misc_data
        return should_update_customer_misc_data

    def get_or_create_customer(self, account: Optional[Account], business_name: str, code: int, contact_id: int):
        customer = None
        is_customer_new = False
        if code is not None and self.is_integer(code):
            customer = Party.objects.filter(partypk=code).first()
        elif account.name:
            # best effort to match by account name since erp code is empty or invalid
            potential_customer: Party = Party.objects.filter(name=account.name).first()
            if potential_customer:
                existing_accounts = AccountList.filter(erp_code=potential_customer.partypk)
                if len(existing_accounts) == 0:
                    # if the erp code is not already in use for paperless parts, assign to the account being used
                    customer = potential_customer
                    update_account_erp_code(self._exporter._integration, account.id, customer.partypk)
        if customer is None:
            logger.info(f'No Party (customer) record found with primary key {code}. Creating one')
            customer: Party = create_customer(business_name, self._exporter.erp_config.company_division_pk)
            is_customer_new = True
            new_erp_code = customer.partypk
            logger.info(f'Created new Party (customer) record with primary key {new_erp_code}')
            if account is None:
                # If no account exists in Paperless Parts, create one
                create_new_paperless_parts_account(self._exporter._integration, new_erp_code, business_name, contact_id)
            elif not IS_TEST:
                # Set the ERP Code to the ID that was generated for this newly created customer
                account_id = account.id
                update_account_erp_code(self._exporter._integration, account_id, new_erp_code)
        return customer, is_customer_new

    @staticmethod
    def is_integer(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

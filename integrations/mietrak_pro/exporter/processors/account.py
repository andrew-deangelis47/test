from typing import Union

from paperless.objects.orders import Order
from paperless.objects.quotes import Quote
from paperless.objects.customers import Account
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException


class AccountProcessor:

    @classmethod
    def process_account_info(cls, quote_or_order: Union[Quote, Order]):
        account = None
        erp_code = None
        business_name = '{}, {}'.format(quote_or_order.contact.last_name, quote_or_order.contact.first_name)
        customer_notes = None
        contact_id = quote_or_order.contact.id
        if quote_or_order.contact.account:
            account_id = quote_or_order.contact.account.id
            # Not all of the information we need to instantiate a customer in MIE Trak Pro is present in the OrderAccount object
            # Pull down the full Account object by ID to get the rest of the information we need
            try:
                account = Account.get(account_id)
            except Exception:
                raise CancelledIntegrationActionException("Account not found in Paperless, throwing error")
            business_name = account.name
            erp_code = account.erp_code
            customer_notes = account.notes

        return account, business_name, erp_code, customer_notes, contact_id

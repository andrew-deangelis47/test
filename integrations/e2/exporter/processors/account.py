from paperless.objects.orders import Order


class AccountProcessor:

    @classmethod
    def process_account_info(cls, order: Order):
        erp_code = None
        business_name = '{}, {}'.format(order.contact.last_name, order.contact.first_name)
        payment_terms = None
        payment_terms_period = None
        customer_notes = None
        account_id = None
        contact_id = order.contact.id
        if order.contact.account:
            business_name = order.contact.account.name
            erp_code = order.contact.account.erp_code
            payment_terms = order.contact.account.payment_terms
            payment_terms_period = order.contact.account.payment_terms_period
            customer_notes = order.contact.account.notes
            account_id = order.contact.account.id
        return business_name, erp_code, payment_terms, payment_terms_period, customer_notes, account_id, contact_id

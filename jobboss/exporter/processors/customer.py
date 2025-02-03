from jobboss.query.customer import get_or_create_customer
import jobboss.models as jb
from . import JobBossProcessor
from paperless.objects.orders import Order


class CustomerProcessor(JobBossProcessor):
    # We don't want to rollback customer records on errors
    do_rollback = False

    def _process(self, order: Order):
        # get customer, bill to info, ship to info
        erp_code = None
        business_name = '{}, {}'.format(order.customer.last_name, order.customer.first_name)
        if order.customer.company:
            business_name = order.customer.company.business_name
            erp_code = order.customer.company.erp_code

        customer: jb.Customer = get_or_create_customer(business_name, erp_code)
        return customer

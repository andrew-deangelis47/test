import jobboss.models as jb
import attr
from jobboss.query.customer import get_or_create_address
from paperless.objects.orders import Order
from jobboss.exporter.processors import JobBossProcessor


class AddressProcessor(JobBossProcessor):
    do_rollback = False

    def _process(self, order: Order, customer: jb.Customer):
        bill_to = self.get_billing_info(order, customer)
        ship_to = self.get_shipping_info(order, customer)
        return bill_to, ship_to

    def get_billing_info(self, order: Order, customer: jb.Customer):
        bill_to = None
        if order.billing_info is not None:
            bill_to: jb.Address = get_or_create_address(
                customer,
                attr.asdict(order.billing_info),
                is_shipping=False
            )
        return bill_to

    def get_shipping_info(self, order: Order, customer: jb.Customer):
        ship_to = None
        if order.shipping_info is not None:
            ship_to: jb.Address = get_or_create_address(
                customer,
                attr.asdict(order.shipping_info),
                is_shipping=True
            )
        return ship_to

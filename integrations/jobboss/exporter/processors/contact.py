import jobboss.models as jb
from jobboss.query.customer import get_or_create_contact
from . import JobBossProcessor
from paperless.objects.orders import Order
from baseintegration.datamigration import logger
from baseintegration.utils import safe_get, trim_django_model


class ContactProcessor(JobBossProcessor):
    do_rollback = False

    def _process(self, order: Order, customer: jb.Customer, bill_to):
        contact_bill_name = order.billing_info.attention if order.billing_info is not None else f'{order.contact.first_name} {order.contact.last_name} '
        contact: jb.Contact = get_or_create_contact(customer, contact_bill_name)
        contact.address = safe_get(bill_to, 'address')
        try:
            contact = trim_django_model(contact)
            contact.save()
        except Exception as e:
            logger.error(f"Failed to save Contact: {contact.contact_name}. [ERROR]: {e}")
            logger.error(contact.__dict__)
        return contact

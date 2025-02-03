from e2.exporter.processors import E2Processor
from baseintegration.datamigration import logger
from e2.models import CustomerCode, Contacts
from paperless.objects.orders import Order


class ContactProcessor(E2Processor):
    do_rollback = False

    def _process(self, order: Order, customer: CustomerCode):
        code = customer.customer_code
        contact_name = f'{order.contact.first_name} {order.contact.last_name}'.upper()
        phone = order.contact.phone
        email = order.contact.email
        extension = order.contact.phone_ext
        comments = order.contact.notes

        contact = self.get_or_create_contact(code, contact_name, phone, email, extension, comments, is_vendor=False)
        return contact

    def get_or_create_contact(self, code, contact_name, phone, email, extension, comments, is_vendor=False):
        contact = self.get_contact_by_email(email)
        if contact is not None:
            logger.info(f'Found existing Contacts record with email {email}')
        else:
            logger.info(f'No Contacts record found with email {email} - creating one')
            contact = self.create_contact(code, contact_name, phone, email, extension, comments, is_vendor)

        return contact

    @staticmethod
    def create_contact(code, contact_name, phone, email, extension, comments, is_vendor=False):
        if is_vendor:
            object = 'VEND'
        else:
            object = 'CUST'

        contact = Contacts.objects.create(
            object=object,
            code=code,
            contact=contact_name,
            phone=phone,
            email=email,
            extension=extension,
            comments=comments,
            active='Y'
        )
        return contact

    @staticmethod
    def get_contact_by_email(email: str):
        """
        Searches E2 for contacts with the same email address.

        Returns the most recently updated one.
        :param email: str
        :return: Contacts
        """
        return Contacts.objects.filter(email__iexact=email) \
            .order_by('-last_mod_date') \
            .first()

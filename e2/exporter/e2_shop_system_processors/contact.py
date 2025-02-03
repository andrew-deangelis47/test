from e2.exporter.processors.contact import ContactProcessor
from e2.models import Contacts


class E2ShopSystemContactProcessor(ContactProcessor):

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
            active='Y',
            counter='123'  # this will get removed the model
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
            .first()

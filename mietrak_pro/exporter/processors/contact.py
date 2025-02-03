from typing import Optional, Union

from mietrak_pro.query.contact import get_contact_for_customer_by_email, create_contact
from mietrak_pro.exporter.processors import MietrakProProcessor
from baseintegration.datamigration import logger
from mietrak_pro.models import Party, Partybuyer
from paperless.objects.orders import Order, OrderContact
from paperless.objects.quotes import Quote, Contact
from baseintegration.utils import trim_django_model


class ContactProcessor(MietrakProProcessor):
    do_rollback = False

    def _process(self, quote_or_order: Union[Quote, Order], customer: Party):
        contact_name = f'{quote_or_order.contact.first_name} {quote_or_order.contact.last_name}'

        email = quote_or_order.contact.email
        notes = quote_or_order.contact.notes

        contact, contact_is_new, party_buyer = self.get_or_create_contact(customer, contact_name, email)

        # If desired, update the internal contact notes
        should_update_contact_notes = self.should_update_mietrak_pro_contact_notes(contact_is_new)
        if should_update_contact_notes:
            self.update_contact_notes(contact, party_buyer, notes)

        # If desired, update the miscellaneous data for the contact
        should_update_contact_misc_data = self.should_update_mietrak_pro_contact_misc_data(contact_is_new)
        if should_update_contact_misc_data:
            self.update_miscellaneous_contact_data(contact, quote_or_order.contact)

        return contact

    def get_or_create_contact(self, customer: Party, contact_name: str, email: str):
        contact, party_buyer = get_contact_for_customer_by_email(customer, email)
        contact_is_new = False
        if contact is not None:
            logger.info(f'Found existing Party (contact) record for customer {customer.name} with email {email}')
        else:
            logger.info(
                f'No Party (contact) record found with email {email} for customer {customer.name} - creating one')
            contact, party_buyer = create_contact(customer, contact_name, email,
                                                  self._exporter.erp_config.company_division_pk)
            contact_is_new = True

        return contact, contact_is_new, party_buyer

    def get_contact_phone(self, quote_or_order_contact: Union[OrderContact, Contact]):
        phone = quote_or_order_contact.phone
        extension = quote_or_order_contact.phone_ext
        if extension:
            phone_with_ext = f'{phone} x{extension}'
        else:
            phone_with_ext = phone
        return phone_with_ext

    def update_contact_notes(self, contact: Party, party_buyer: Partybuyer, contact_notes: Optional[str]):
        if contact_notes is not None:
            logger.info('Updating contact notes')
            party_buyer.description = contact_notes
            party_buyer = trim_django_model(party_buyer)
            party_buyer.save()

    def update_miscellaneous_contact_data(self, contact: Party, quote_or_order_contact: Union[OrderContact, Contact]):
        contact.phone = self.get_contact_phone(quote_or_order_contact)
        contact.save()

    def should_update_mietrak_pro_contact_notes(self, contact_is_new: bool):
        should_update_contact_notes = \
            contact_is_new or self._exporter.erp_config.should_update_mietrak_pro_contact_notes
        return should_update_contact_notes

    def should_update_mietrak_pro_contact_misc_data(self, contact_is_new: bool):
        should_update_contact_misc_data = \
            contact_is_new or self._exporter.erp_config.should_update_mietrak_pro_contact_misc_data
        return should_update_contact_misc_data

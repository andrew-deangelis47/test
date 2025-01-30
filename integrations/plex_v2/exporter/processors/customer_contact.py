from plex_v2.exporter.processors.base import PlexProcessor
from plex_v2.objects.customer import Customer, CustomerContact
from paperless.objects.orders import Order
from plex_v2.factories.plex.customer_contact import PlexCustomerContactFactory
from plex_v2.utils.export import ExportUtils


class ContactProcessor(PlexProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'customer'

    def _process(self, order: Order, customer: Customer, customer_contact_factory: PlexCustomerContactFactory, utils: ExportUtils) -> CustomerContact:
        """
        returns existing plex contact if it exists, otherwise create
        """

        can_create_new_customers = self.config.can_creat_new_customers

        # check for existing contact
        existing_contact, last_sort_order = utils.get_existing_plex_contact_and_sort_order(order, customer)
        if existing_contact is not None:
            self._add_report_message(f'Using existing contact email="{existing_contact.email}"')
            return existing_contact

        # create if not already existing
        if can_create_new_customers:
            contact = customer_contact_factory.to_customer_contact(order.contact, customer, last_sort_order)
            contact.create()
            self._add_report_message(f'Created new contact "{contact.email}"')
            return contact

        return None

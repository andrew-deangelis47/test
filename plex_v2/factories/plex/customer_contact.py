from plex_v2.factories.base import BaseFactory
from paperless.objects.orders import OrderContact
from plex_v2.objects.customer import Customer, CustomerContact


class PlexCustomerContactFactory(BaseFactory):

    def to_customer_contact(self, contact: OrderContact, customer: Customer, last_sort_order: int) -> CustomerContact:
        return CustomerContact(
            email=contact.email,
            customerId=customer.id,
            firstName=contact.first_name,
            lastName=contact.last_name,
            phone=contact.phone,
            note=contact.notes,
            sortOrder=last_sort_order + 1,
            private=0
        )

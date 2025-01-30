from plex_v2.configuration import PlexConfig
from plex_v2.objects.customer import CustomerContact
from paperless.objects.customers import Contact
import re


class ContactFactory:

    def __init__(self, config: PlexConfig):
        self.config: PlexConfig = config

    def to_paperless_contact(self, plex_contact: CustomerContact, erp_code: str) -> Contact:
        return Contact(
            account_id=erp_code,
            first_name=plex_contact.firstName,
            last_name=plex_contact.lastName,
            email=plex_contact.email,
            phone=self._scrub_phone_number(plex_contact.phone),
            notes=plex_contact.note
        )

    def _scrub_phone_number(self, phone_num: str):
        return re.sub('[^0-9]', '', phone_num)[0:10]

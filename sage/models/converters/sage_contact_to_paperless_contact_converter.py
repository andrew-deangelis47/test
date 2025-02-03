from sage.models.sage_models.customer.contact import Contact as SageContact
from paperless.objects.customers import Contact as PaperlessContact


class SageContactToPaperlessContactConverter:

    @staticmethod
    def to_paperless_contact(sage_contact: SageContact, account_id: int) -> PaperlessContact:
        # we need the following (at a min) in order to create a paperless contact:
        #   - account id
        #   - email
        #   - first_name
        #   - last_name

        account_id = account_id
        email = sage_contact.email
        first_name = sage_contact.first_name
        last_name = sage_contact.last_name

        paperless_contact = PaperlessContact(
            account_id,
            email,
            first_name,
            last_name
        )

        return paperless_contact

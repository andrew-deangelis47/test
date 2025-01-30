from sage.models.sage_models.customer.address import Address as SageAddress
from paperless.objects.customers import Address as PaperlessAddress
from baseintegration.utils.address import AddressUtils


class SageAddressToPaperlessAddressConverter:

    @staticmethod
    def to_paperless_address(sage_address: SageAddress, customer_code: str) -> PaperlessAddress:
        country_alpha_3, state_province_name = AddressUtils.get_country_and_state(
            sage_address.country,
            sage_address.state,
            sage_address.zip_code,
        )

        paperless_address = PaperlessAddress
        paperless_address.address1 = sage_address.address_line_1
        paperless_address.address2 = sage_address.address_line_2
        paperless_address.city = sage_address.city
        paperless_address.state = state_province_name
        paperless_address.country = country_alpha_3
        paperless_address.postal_code = sage_address.zip_code
        paperless_address.erp_code = customer_code

        return paperless_address

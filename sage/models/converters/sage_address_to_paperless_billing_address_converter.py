from sage.models.sage_models.customer.address import Address as SageAddress
from paperless.objects.customers import BillingAddress as PaperlessBillingAddress
from baseintegration.utils.address import AddressUtils


class SageAddressToPaperlessBillingAddressConverter:

    @staticmethod
    def to_paperless_billing_address(sage_address: SageAddress, customer_code: str) -> PaperlessBillingAddress:
        country_alpha_3, state_province_name = AddressUtils.get_country_and_state(
            sage_address.country,
            sage_address.state,
            sage_address.zip_code,
        )

        paperless_billing_address = PaperlessBillingAddress(
            address1=sage_address.address_line_1,
            city=sage_address.city,
            state=state_province_name,
            country=country_alpha_3,
            postal_code=sage_address.zip_code,
            erp_code=customer_code
        )

        # only set address 2 if it is not a blank string
        if len(sage_address.address_line_2.strip()) > 0:
            paperless_billing_address.address2 = sage_address.address_line_2

        return paperless_billing_address

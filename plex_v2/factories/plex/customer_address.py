from plex_v2.objects.customer import Customer, CustomerAddress
from paperless.objects.address import AddressInfo
from plex_v2.factories.base import BaseFactory


class PlexCustomerAddressFactory(BaseFactory):

    def to_plex_customer_address(self, customer: Customer, address_info: AddressInfo, is_shipping_address: bool, alt_code: str) -> CustomerAddress:
        """
        if is_shipping_address is False then we consider this a billing address
        we have different logic for these two scenarios
        """

        return CustomerAddress(
            address=self._get_address(address_info),
            city=address_info.city,
            state=address_info.state,
            zip=address_info.postal_code,
            country=address_info.country,
            customerId=customer.id,
            active=True,
            code=alt_code,
            phone=address_info.phone,
            billTo=self._get_bill_to(is_shipping_address),
            shipTo=self._get_ship_to(is_shipping_address),
            remitTo=self._get_remit_to(is_shipping_address),
            soldTo=self._get_sold_to(is_shipping_address),
        )

    def _get_code(self, address_info: AddressInfo) -> str:
        if address_info.facility_name is not None:
            return address_info.facility_name
        return ''

    def _get_address(self, address_info: AddressInfo) -> str:
        return f'{address_info.address1} {address_info.address2}'

    def _get_bill_to_address_id(self, is_shipping_address: bool) -> str:
        if is_shipping_address:
            return 'Shipping'

        return 'Billing'

    def _get_bill_to(self, is_shipping_address: bool) -> bool:
        if is_shipping_address:
            return False
        return True

    def _get_ship_to(self, is_shipping_address: bool) -> bool:
        if is_shipping_address:
            return True
        return False

    def _get_remit_to(self, is_shipping_address: bool) -> bool:
        if is_shipping_address:
            return False
        return True

    def _get_sold_to(self, is_shipping_address: bool) -> bool:
        if is_shipping_address:
            return False
        return True

from paperless.objects.customers import Facility as PaperlessFacility
from sage.models.sage_models.customer.customer_full_entity import SageCustomerFullEntity
from sage.models.sage_models.customer.address import Address as SageAddress
from sage.models.converters.sage_address_to_paperless_address_converter import SageAddressToPaperlessAddressConverter
from baseintegration.datamigration import logger
from typing import Union


def get_sage_address_by_key(key: str, sage_addresses: list) -> SageAddress:
    for sage_address in sage_addresses:
        if sage_address.address_id == key:
            return sage_address
    return None


def _is_blank(some_str: str) -> bool:
    return len(some_str.strip()) == 0


def _validate_sage_address(sage_address: SageAddress) -> bool:
    # Assign address attributes
    address_fields = (
        sage_address.address_line_1,
        sage_address.city,
        sage_address.state,
        sage_address.zip_code
    )

    # Check if address has enough criteria for Paperless Parts address validation
    not_none = all([field is not None for field in address_fields])
    not_blank = all([not _is_blank(field) for field in address_fields])
    return not_blank and not_none


class SageCustomerToPaperlessFacilityConverter:

    @staticmethod
    def to_paperless_facility(sage_full_customer_entity: SageCustomerFullEntity, paperless_account_id: int) -> Union[PaperlessFacility, bool]:
        # 1) find the correct address to use for facility
        sage_ship_to_addr = get_sage_address_by_key(
            sage_full_customer_entity.customer.default_ship_to_address,
            sage_full_customer_entity.addresses
        )

        # 2) check to make sure this is a valid address
        if not _validate_sage_address(sage_ship_to_addr):
            logger.warning('Ship to address is invalid')
            return False

        # create facility from address info
        paperless_facility = PaperlessFacility()
        paperless_facility.address = SageAddressToPaperlessAddressConverter.to_paperless_address(sage_ship_to_addr, sage_full_customer_entity.customer.code)
        paperless_facility.account_id = paperless_account_id
        paperless_facility.attention = ''
        paperless_facility.name = sage_ship_to_addr.description

        return paperless_facility

    @staticmethod
    def update_existing_facility(paperless_facility: PaperlessFacility, sage_full_customer_entity: SageCustomerFullEntity) -> Union[PaperlessFacility, bool]:
        # 1) find the correct address to use for facility
        sage_ship_to_addr = get_sage_address_by_key(
            sage_full_customer_entity.customer.default_ship_to_address,
            sage_full_customer_entity.addresses
        )

        # 2) check to make sure this is a valid address
        if not _validate_sage_address(sage_ship_to_addr):
            logger.warning('Ship to address is invalid')
            return False

        # 3) update existing facility info
        paperless_facility.address = SageAddressToPaperlessAddressConverter.to_paperless_address(sage_ship_to_addr, sage_full_customer_entity.customer.code)
        paperless_facility.attention = ''
        paperless_facility.name = sage_ship_to_addr.description

        return paperless_facility

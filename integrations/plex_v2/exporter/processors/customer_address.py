from plex_v2.exporter.processors.base import PlexProcessor
from paperless.objects.orders import AddressInfo
from plex_v2.objects.customer import Customer, CustomerAddress
from baseintegration.integration.cancelled_integration_action_exception import CancelledIntegrationActionException
from plex_v2.utils.export import ExportUtils
from plex_v2.factories.plex.customer_address import PlexCustomerAddressFactory
from typing import Union


class CustomerAddressProcessor(PlexProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'customer'

    def _process(
            self,
            customer: Customer,
            utils: ExportUtils,
            factory: PlexCustomerAddressFactory,
            address_info: AddressInfo,
            address_functions,
            code_suffix,
            billing_address_id=None
    ):

        is_shipping_address = code_suffix == 'Shipping'
        address_functions_kwargs = {func: True for func in address_functions}

        if address_info is None:
            if not self.config.use_plex_address_as_fallback:
                raise CancelledIntegrationActionException(
                    f'No {code_suffix} address on the Paperless Parts order and integration is not configured to use Plex address as fallback')

            plex_address: CustomerAddress = utils.get_existing_plex_address(customer, address_functions, code_suffix)
            self._add_report_message(f'Found existing {code_suffix} address in Plex, code is {plex_address.code}')
            return plex_address

        # get an alt code for the address if we have address info
        alt_code = utils.get_plex_address_alt_code_from_address_info(address_info, code_suffix)

        if utils.has_facility_name(address_info):
            plex_address: CustomerAddress = utils.use_facility_name_to_get_address(customer, address_info, address_functions, billing_address_id)
            self._add_report_message(f'Found existing {code_suffix} address in Plex, code is {plex_address.code}')
            return plex_address

        else:
            plex_address: Union[CustomerAddress, None] = utils.get_customer_address_by_alt_code(customer, alt_code)
            if plex_address:
                self._add_report_message(f'{code_suffix} address code is {plex_address.code}')
                return plex_address

        address_to_create: CustomerAddress = factory.to_plex_customer_address(customer, address_info, is_shipping_address, alt_code)
        plex_address: CustomerAddress = utils.create_address_if_no_match(customer, address_to_create, address_functions_kwargs)
        self._add_report_message(f'{code_suffix} address code is {plex_address.code}')
        return plex_address

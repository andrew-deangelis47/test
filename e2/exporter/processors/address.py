from typing import Optional

import e2.models as e2
from e2.query.address import create_shipping_address, match_shipping_address, get_shipping_address_by_location
from paperless.objects.orders import Order
from e2.exporter.processors import E2Processor
from baseintegration.datamigration import logger
from e2.utils.utils import create_addr_dict


class AddressProcessor(E2Processor):
    do_rollback = False

    def _process(self, order: Order, customer: e2.CustomerCode, customer_is_new: bool):
        ship_to = self.get_shipping_info(order, customer, customer_is_new)
        return ship_to

    def get_shipping_info(self, order: Order, customer: e2.CustomerCode, customer_is_new: bool):
        # TODO - what to do about shipvia? It looks like this should reference the ShippingDescription field in the ShipMethod table
        if order.shipping_info is not None:
            shipping_addr_dict = self.create_shipping_addr_dict(order.shipping_info)
            should_create_shipping_address = self.should_create_e2_shipping_address(customer_is_new)
            if should_create_shipping_address:
                ship_to: e2.Shipto = self.get_or_create_shipping_address(
                    customer,
                    shipping_addr_dict,
                )
            else:
                # If the user doesn't want us to create new shipping addresses in E2, just try to match on existing ones
                ship_to: Optional[e2.Shipto] = match_shipping_address(
                    customer,
                    shipping_addr_dict
                )
            return ship_to
        else:
            # If a shipping address is not supplied on the Paperless Parts order, try to use the default shipping
            # address for this customer in E2
            default_ship_to = None
            default_location = customer.location
            if default_location is not None:
                default_ship_to = get_shipping_address_by_location(customer, default_location)
            return default_ship_to

    def should_create_e2_shipping_address(self, customer_is_new: bool):
        should_create_shipping_address = customer_is_new or self._exporter.erp_config.should_create_e2_shipping_address
        return should_create_shipping_address

    def get_or_create_shipping_address(self, customer: e2.CustomerCode, addr_dict: dict):
        """ Try to match on the facility name first. If that doesn't work, try matching based on the address fields. """
        shipping_address = None
        facility_name = addr_dict.get('facility_name')
        if facility_name is not None:
            shipping_address = get_shipping_address_by_location(customer, facility_name)
        if shipping_address is None:
            shipping_address = match_shipping_address(customer, addr_dict)
        if shipping_address is not None:
            logger.info('Found matching shipping address')
        else:
            logger.info('Could not find matching shipping address - creating one')
            shipping_address = create_shipping_address(customer, addr_dict)
        return shipping_address

    def create_shipping_addr_dict(self, shipping_info):
        return create_addr_dict(shipping_info)

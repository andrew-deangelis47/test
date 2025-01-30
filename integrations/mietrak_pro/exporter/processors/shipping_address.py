from typing import Optional, Union

import mietrak_pro.models
from mietrak_pro.query.address import create_shipping_address, match_shipping_address
from paperless.objects.orders import Order
from paperless.objects.quotes import Quote
from mietrak_pro.exporter.processors import MietrakProProcessor
from baseintegration.datamigration import logger
from mietrak_pro.exporter.utils import create_addr_dict


class ShippingAddressProcessor(MietrakProProcessor):
    do_rollback = False

    def _process(self, quote_or_order: Union[Quote, Order], customer: mietrak_pro.models.Party, is_customer_new):
        shipping_address = self.get_shipping_info(quote_or_order, customer, is_customer_new)
        return shipping_address

    def get_shipping_info(self, quote_or_order: Union[Quote, Order], customer: mietrak_pro.models.Party,
                          is_customer_new):
        if quote_or_order.shipping_info is not None:
            shipping_addr_dict = self.create_shipping_addr_dict(quote_or_order.shipping_info)
            should_create_shipping_address = self.should_create_mietrak_pro_shipping_address(is_customer_new)
            if should_create_shipping_address:
                shipping_address = self.get_or_create_shipping_address(
                    customer,
                    shipping_addr_dict,
                )
            else:
                # If the user doesn't want us to create new shipping addresses in MIE Trak Pro, just try to match on existing ones
                shipping_address: Optional[mietrak_pro.models.ShippingAddress] = match_shipping_address(
                    customer,
                    shipping_addr_dict
                )
            return shipping_address
        else:
            return None

    def should_create_mietrak_pro_shipping_address(self, is_customer_new):
        should_create_shipping_address = \
            is_customer_new or self._exporter.erp_config.should_create_mietrak_pro_shipping_address
        return should_create_shipping_address

    def get_or_create_shipping_address(self, customer, addr_dict):
        shipping_address = match_shipping_address(customer, addr_dict)
        if shipping_address is not None:
            logger.info('Found matching shipping address')
        else:
            logger.info('Could not find matching shipping address - creating one')
            shipping_address = create_shipping_address(customer, addr_dict,
                                                       self._exporter.erp_config.company_division_pk)
        return shipping_address

    def create_shipping_addr_dict(self, shipping_info):
        return create_addr_dict(shipping_info)

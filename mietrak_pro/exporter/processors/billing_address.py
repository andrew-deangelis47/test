from typing import Optional, Union

from mietrak_pro.models import Party, BillingAddress
from mietrak_pro.query.address import create_billing_address, match_billing_address
from paperless.objects.orders import Order
from paperless.objects.quotes import Quote
from mietrak_pro.exporter.processors import MietrakProProcessor
from baseintegration.datamigration import logger
from mietrak_pro.exporter.utils import create_addr_dict


class BillingAddressProcessor(MietrakProProcessor):
    do_rollback = False

    def _process(self, quote_or_order: Union[Quote, Order], customer: Party, is_customer_new: bool):
        billing_address = self.get_billing_info(quote_or_order, customer, is_customer_new)
        return billing_address

    def get_billing_info(self, quote_or_order: Union[Quote, Order], customer: Party, is_customer_new: bool):
        if quote_or_order.billing_info is not None:
            billing_addr_dict = self.create_billing_addr_dict(quote_or_order.billing_info)
            should_create_billing_address = self.should_create_mietrak_pro_billing_address(is_customer_new)
            if should_create_billing_address:
                billing_address = self.get_or_create_billing_address(
                    customer,
                    billing_addr_dict,
                )
            else:
                # If the user doesn't want us to create new billing addresses in MIE Trak Pro, just try to match on existing ones
                billing_address: Optional[BillingAddress] = match_billing_address(
                    customer,
                    billing_addr_dict
                )
            return billing_address
        else:
            return None

    def should_create_mietrak_pro_billing_address(self, is_customer_new: bool):
        should_create_billing_address = \
            is_customer_new or self._exporter.erp_config.should_create_mietrak_pro_billing_address
        return should_create_billing_address

    def get_or_create_billing_address(self, customer: Party, addr_dict: dict):
        billing_address = match_billing_address(customer, addr_dict)
        if billing_address is not None:
            logger.info('Found matching billing address')
        else:
            logger.info('Could not find matching billing address - creating one')
            billing_address = create_billing_address(customer, addr_dict, self._exporter.erp_config.company_division_pk)
        return billing_address

    def create_billing_addr_dict(self, billing_info):
        return create_addr_dict(billing_info)

from plex_v2.exporter.processors.base import PlexProcessor
from plex_v2.objects.sales_orders import SalesOrder, SalesOrder2Tier
from paperless.objects.orders import Order
from plex_v2.objects.customer import Customer
from baseintegration.datamigration import logger
from typing import Union, Tuple
from plex_v2.utils.export import ExportUtils
from plex_v2.factories.plex.sales_order import SalesOrderFactory


class SalesOrderProcessor(PlexProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'sales_order'

    def _process(
            self,
            order: Order,
            customer: Customer,
            tier: str,
            po_number: str,
            quote_num_w_rev: str,
            billToAddressId: str,
            shipToAddressId: str,
            utils: ExportUtils,
            sales_order_factory: SalesOrderFactory
    ) -> Tuple[SalesOrder, str, str]:

        # 1) get tier and existing order with this customer and po number
        existing_sales_order: SalesOrder = utils.get_existing_sales_order_by_po_number_and_customer(
            po_number,
            customer
        )

        # 2) If order already exists and tier 3, we return the existing sales order
        #    as tier 3 orders do not allow for multiple POs
        if existing_sales_order and tier == 3:
            message = 'Found existing customer PO with PO number "{}"\n'.format(po_number)
            self._add_report_message(message)
            logger.info(message)
            return existing_sales_order

        # 3) create model for either tier 2 or tier 3 sales order
        sales_order: Union[SalesOrder, SalesOrder2Tier] = self._get_sales_order_model_based_on_tier(
            tier,
            customer,
            billToAddressId,
            shipToAddressId,
            order,
            sales_order_factory,
            po_number,
            quote_num_w_rev
        )

        # 4) create sales order in Plex if it does not exist
        sales_order: Union[SalesOrder, SalesOrder2Tier] = utils.create_sales_order_if_not_already_exists(
            sales_order,
            existing_sales_order,
            order,
            po_number
        )

        # 5) log
        if existing_sales_order:
            self._add_report_message(f'Found existing sales order for customer with po# {existing_sales_order.poNumber}')
        else:
            self._add_report_message(f'Created sales order with po# {sales_order.poNumber}')

        return sales_order

    def _get_sales_order_model_based_on_tier(self, tier: int, customer: Customer, billToAddressId: str, shipToAddressId: str, pp_order: Order, sales_order_factory: SalesOrderFactory, po_number: str, quote_number_with_revision: str) -> SalesOrder:
        # tier 2
        if tier == 2:
            return sales_order_factory.to_tier_2_sales_order(
                po_number,
                customer,
                billToAddressId,
                shipToAddressId,
                pp_order,
                quote_number_with_revision
            )

        # tier 3
        return sales_order_factory.to_tier_3_sales_order(
            po_number,
            customer,
            billToAddressId,
            shipToAddressId,
            pp_order,
            quote_number_with_revision
        )

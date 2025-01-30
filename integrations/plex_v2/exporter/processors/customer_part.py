from plex_v2.exporter.processors.base import PlexProcessor
from paperless.objects.orders import OrderItem, OrderComponent
from plex_v2.utils.export import ExportUtils
from plex_v2.objects.customer import Customer, CustomerPart
from baseintegration.datamigration import logger
from plex_v2.objects.part import Part
from plex_v2.factories.plex.customer_part import CustomerPartFactory
from plex_v2.objects.plex_part_to_plex_customer_part_mapping import PlexPartToPlexCustomerPartMapping


class CustomerPartProcessor(PlexProcessor):

    INTEGRATION_EXPORT_REPORT_COLUMN_NAME = 'customer_part'

    def _process(self, order_item: OrderItem, customer: Customer, utils: ExportUtils, customer_part_factory: CustomerPartFactory):
        """
        iterate through the top level parts, create customer part, return the part/customer part pairings
        """

        # grab the top level part
        top_level_part: OrderComponent = utils.get_top_level_part_from_order_item(order_item)
        plex_top_level_part: Part = utils.get_plex_part_from_paperless_component(top_level_part)

        # use existing customer part if exists
        existing_customer_part = utils.get_customer_part_if_exists(plex_top_level_part, customer)
        if existing_customer_part is not None:
            mapping: PlexPartToPlexCustomerPartMapping = self._handle_using_existing_customer_part(existing_customer_part, plex_top_level_part, order_item, customer)
            self._add_report_message(f'Using existing customer part with number {existing_customer_part.number}')
        else:
            # if there is no existing customer part, create it
            mapping: PlexPartToPlexCustomerPartMapping = self._handle_using_new_customer_part(plex_top_level_part, customer, order_item, customer_part_factory)
            self._add_report_message(f'Created customer part with number {mapping.customer_part.number}')

        return mapping

    def _handle_using_existing_customer_part(self, existing_customer_part: CustomerPart, plex_top_level_part: Part, order_item: OrderItem, customer: Customer):
        logger.info(f'Using existing customer part, number={existing_customer_part.number}, customer={customer.name}')
        # return the part to customer part mapping
        mapping = PlexPartToPlexCustomerPartMapping(plex_top_level_part, existing_customer_part, order_item)
        return mapping

    def _handle_using_new_customer_part(self, plex_top_level_part: Part, customer: Customer, order_item: OrderItem, customer_part_factory: CustomerPartFactory):
        # create customer part
        customer_part: CustomerPart = customer_part_factory.to_customer_part(plex_top_level_part, customer)
        customer_part.create()

        # return the part to customer part mapping
        mapping = PlexPartToPlexCustomerPartMapping(plex_top_level_part, customer_part, order_item)
        return mapping

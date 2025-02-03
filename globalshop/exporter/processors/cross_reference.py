from typing import Optional

from baseintegration.datamigration import logger
from globalshop.cross_reference import CrossReference
from globalshop.customer import CustomerRecord
from paperless.objects.orders import OrderItem, OrderComponent, Order
from globalshop.exporter.processors import GSProcessor


class CrossReferenceProcessor(GSProcessor):

    def _process(self, item: OrderItem, order: Order,
                 customer_record: CustomerRecord = None):

        """
        We are going to write out the part level information every time,
        as the settings for when to update/insert a record is controlled
        inside Global Shop
        """
        root = item.root_component

        for assm_component in item.iterate_assembly():
            self._insert_component_xref(root, assm_component.component,
                                        item, order, customer_record)

    def _insert_component_xref(self, root: OrderComponent,
                               component: OrderComponent,
                               line_item: OrderItem,
                               order: Order = None,
                               customer_record: CustomerRecord = None):
        if component.part_number is not None:
            part_num = component.part_number
        else:
            part_num = component.part_name
        external_partnumber = part_num
        partnumber = part_num
        revision = component.revision
        customer = None
        logger.info(f'erpcode {customer}')
        if customer_record:
            customer = customer_record.gss_customer_number
        customer_part = self._get_customer_part(root, component, line_item, order)
        vendor = None
        manufacturer_part = None
        manufacturer_name = None
        status = None
        user_default_title = None
        comment = None

        CrossReference.insert(external_partnumber=external_partnumber,
                              partnumber=partnumber,
                              revision=revision,
                              customer=customer,
                              customer_part=customer_part,
                              vendor=vendor,
                              manufacturer_part=manufacturer_part,
                              manufacturer_name=manufacturer_name,
                              status=status,
                              user_default_title=user_default_title,
                              comment=comment)

    def _get_customer_part(self, root: OrderComponent, component: OrderComponent, line_item: OrderItem,
                           order: Order = None) -> Optional[str]:
        # Override for customer until we have some default behavior
        return None

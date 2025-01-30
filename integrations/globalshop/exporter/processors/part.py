from decimal import Decimal
from typing import Optional

from baseintegration.datamigration import logger
from globalshop.customer import CustomerRecord
from paperless.objects.orders import OrderItem, OrderComponent, Order
from globalshop.exporter.processors import GSProcessor
from globalshop.part import Part
from baseintegration.utils import set_blank_to_default_value
from utils import pad_part_num


class PartProcessor(GSProcessor):

    def _process(self, item: OrderItem, order: Order,
                 customer_record: CustomerRecord = None):

        """
        We are going to write out the part level information every time,
        as the settings for when to update/insert a record is controlled
        inside Global Shop
        """
        root = item.root_component

        for assm_component in item.iterate_assembly():
            self._insert_component_part(root, assm_component.component,
                                        item, order, customer_record)

    def _insert_component_part(self, root: OrderComponent,
                               component: OrderComponent,
                               line_item: OrderItem,
                               order: Order = None,
                               customer_record: CustomerRecord = None):
        if component.part_number is not None:
            external_partnumber = component.part_number
        else:
            external_partnumber = component.part_name

        revision = self._get_revision(component)

        part_num = pad_part_num(external_partnumber)
        part = Part.get(part_num[:17] + (revision or ''))
        if part is not None:
            logger.info(f'Found part in globalshop {part.part} so not inserting')
            return

        location = ''
        product_line = self._get_product_line(component=component)
        description = self._get_part_description(component=component,
                                                 item=line_item, order=order)
        short_description = set_blank_to_default_value(description, '').split('\n')[0][0:30]
        unit_of_measure = 'EA'
        source = self._get_source(component=component)
        default_bin = ''
        abc_code = ''
        purchasing_um = ''
        lead_time = self._get_lead_time(line_item=line_item, component=component)
        safety_stock = Decimal(0.0)
        # order_quantity = component.innate_quantity
        order_quantity = self._get_order_quantity(component=component)
        sort_code = self._get_sort_code(component=component,
                                        customer_record=customer_record)
        inactive_status = self._get_inactive()
        vendor_code = ''
        user_field_1 = ''
        user_field_2 = ''
        maximum = Decimal(0.0)
        reorder_point = Decimal(0.0)
        length = Decimal(0.0)
        width = Decimal(0.0)
        thickness = Decimal(0.0)
        density = Decimal(0.0)
        weight = Decimal(0.0)
        alt_description_1 = ''
        alt_description_2 = ''
        price = self._get_list_price(component, line_item)
        cost = Decimal(0.0)
        alternate_cost = Decimal(0.0)

        Part.insert(external_partnumber=external_partnumber,
                    partnumber=external_partnumber,
                    revision=revision,
                    location=location,
                    product_line=product_line,
                    description=short_description,
                    unit_of_measure=unit_of_measure,
                    source=source,
                    default_bin=default_bin,
                    abc_code=abc_code,
                    purchasing_um=purchasing_um,
                    lead_time=lead_time,
                    safety_stock=safety_stock,
                    order_quantity=order_quantity,
                    sort_code=sort_code,
                    vendor_sort=vendor_code,
                    user_field_1=user_field_1,
                    user_field_2=user_field_2,
                    maximum=maximum,
                    reorder_point=reorder_point,
                    length=length,
                    width=width,
                    thickness=thickness,
                    density=density,
                    weight=weight,
                    alt_description_1=alt_description_1,
                    alt_description_2=alt_description_2,
                    price=price,
                    cost=cost,
                    alternate_cost=alternate_cost,
                    extra_description=description,
                    inactive=inactive_status
                    )

    def _get_order_quantity(self, component: OrderComponent):
        return Decimal(component.make_quantity)

    def _get_lead_time(self, line_item: OrderItem, component: OrderComponent):
        return int(line_item.lead_days)

    def _get_part_description(self, component: OrderComponent,
                              item: OrderItem, order: Order) -> str:
        """
        Get the description to put on the part
        """
        if component.is_hardware:
            description = self._get_purchased_component_part_description(
                component, item, )
        else:
            description = component.description if component.description \
                else item.description

        return description

    def _get_purchased_component_part_description(self,
                                                  component: OrderComponent,
                                                  item: OrderItem):
        """
        Get a purchased component part description:
        """
        description = component.description
        notes = item.public_notes
        return f"{description} {notes}"

    def _get_list_price(self, component: OrderComponent, item: OrderItem):
        """

        """
        if component.is_root_component and item.quantity == 1:
            # If the selected quantity is 1 then set to unit price, otherwise
            price = item.unit_price.raw_amount
        else:
            price = 0
        # elif component.is_hardware:
        #     pl = 'PP'
        # else:
        #     pl = 'FC'
        return price

    def _get_product_line(self, component: OrderComponent) -> str:
        """
        Most of the time we just want to export this as "FG" or a finished
        good. extra criteria can be overridden in the future.
        """
        pl = None
        if component.is_root_component:
            pl = 'FG'
        elif component.is_hardware:
            pl = 'PP'
        elif component.process.external_name == 'Customer Furnished':
            pl = 'CF'
        else:
            pl = 'FC'
        return pl

    def _get_source(self, component: OrderComponent) -> str:
        """
        Source for FG/FC is Manuf to Job, PP - Purchased to Job
        values are one character: J, P, G, F
        """
        if component.is_root_component:
            # source = 'Manuf to Job'
            source = 'F'
        elif component.is_hardware:
            # source = 'Purch to Job'
            source = 'J'
        elif component.process.external_name == 'Customer Furnished':
            # source = 'Consign to Job'
            source = 'G'
        else:
            # source = 'Manuf to Job'
            source = 'F'
        return source

    def _get_sort_code(self, component: OrderComponent,
                       customer_record: CustomerRecord = None) -> str:
        """
        Get the sort code for a given routing line.
        """
        sort_code = None
        use_cust_sort = self._exporter.erp_config.use_cust_id_as_sort_code
        if use_cust_sort and customer_record:
            # If this is a purchased part, don't set the sort code to be the
            # customer:
            # if component.is_hardware:
            #     sort_code = None
            # else:
            # sort_code = self._exporter.erp_config.cust_sort_code
            sort_code = customer_record.gss_customer_number
        else:
            # TODO: don't know what the other good option would be...
            pass
        return sort_code

    def _get_revision(self, component: OrderComponent) -> Optional[str]:
        return component.revision

    def _get_inactive(self) -> bool:
        return False

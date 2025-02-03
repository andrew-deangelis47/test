from baseintegration.exporter.processor import BaseProcessor
from paperless.objects.orders import Order, OrderItem
from paperless.objects.components import AssemblyComponent, BaseComponent
from baseintegration.datamigration import logger
from typing import List

from sage.models.sage_models.bom.bom_full_entity import BomFullEntity
from sage.sage_api.client import SageImportClient
from sage.models.sage_models.bom import BomHeader, BomDetail


class BomProcessor(BaseProcessor):

    def _process(self, order: Order) -> list:
        self.client = SageImportClient.get_instance()

        for order_item in order.order_items:
            i = self.get_bottom_level(order_item)
            if i == 0:
                bomfull = self.create_top_level_only_bom(order_item)
                self.client.create_bom(bomfull)
            else:
                while i >= 1:
                    bomfull = self.create_bom_entity(order_item, i)
                    logger.error('Creating BOM in Sage: ==========================>')
                    bms = []
                    for bm in bomfull.bom_details:
                        if bm.component == '000-550-001  Black':
                            bm.component = '000-550-001Black'
                        bms.append(bm)
                    bomfull.bom_details = bms
                    self.client.create_bom(bomfull)
                    i -= 1

    def create_top_level_only_bom(self, order_item: OrderItem):
        parent_component_for_level = self.get_top_level_component(order_item)
        if parent_component_for_level.part_number is not None:
            logger.info('Processing Bom with parent component: ' + parent_component_for_level.part_number)
        else:
            logger.info('Processing Bom with parent component: ""')
        logger.info('No components in this Bom')
        bom_header = self.create_top_level_only_bom_header(parent_component_for_level)
        bom_details = self.create_bom_details([])
        return BomFullEntity(bom_details=bom_details, bom_header=bom_header)

    def create_bom_entity(self, order_item: OrderItem, level: int) -> BomFullEntity:
        parent_component_for_level = self.get_parent_component_for_level(order_item, level)
        if parent_component_for_level.part_number is not None:
            logger.info('Processing Bom with parent component: ' + parent_component_for_level.part_number)
        else:
            logger.info('Processing Bom with parent component: ""')
        assembly_components_for_level = self.get_components_for_level(order_item, level)
        bom_header = self.create_bom_header(parent_component_for_level)
        bom_details = self.create_bom_details(assembly_components_for_level)
        comp_str = ""
        for bom_detail in bom_details:
            if bom_detail.component is not None:
                comp_str += bom_detail.component + ', '
        comp_str = comp_str[:-2]
        logger.info('Components: ' + comp_str)
        return BomFullEntity(bom_details=bom_details, bom_header=bom_header)

    def create_top_level_only_bom_header(self, component: BaseComponent):
        bom_header = BomHeader()
        bom_header.parent_product = component.component.part_number
        bom_header.bom_code = component.component.description
        bom_header.base_quantity = component.component.deliver_quantity

        return bom_header

    def create_bom_header(self, component: BaseComponent):
        bom_header = BomHeader()
        bom_header.parent_product = component.part_number
        bom_header.bom_code = component.description
        bom_header.base_quantity = component.deliver_quantity

        return bom_header

    def create_bom_details(self, assembly_components: List[AssemblyComponent]) -> List[BomDetail]:

        bom_details_list = []
        i = 1
        for component in assembly_components:
            bom_details = BomDetail()
            bom_details.revision_group = component.component.revision
            bom_details.component = component.component.part_number
            bom_details.link_quantity = component.component.deliver_quantity

            bom_details_list.append(bom_details)
            i += 1

        return bom_details_list

    def get_parent_component_for_level(self, order_item: OrderItem, level: int) -> BaseComponent:
        for comp in order_item.iterate_assembly():
            if comp.level == level and comp.parent is not None:
                return comp.parent

    def get_top_level_component(self, order_item: OrderItem) -> BaseComponent:
        for comp in order_item.iterate_assembly():
            if comp.component.is_root_component:
                return comp

    def get_components_for_level(self, order_item: OrderItem, level: int) -> List[BaseComponent]:
        comps_for_level = []
        for comp in order_item.iterate_assembly():
            if comp.level == level:
                comps_for_level.append(comp)

        return comps_for_level

    def get_bottom_level(self, order_item: OrderItem) -> int:
        max = 0
        for comp in order_item.iterate_assembly():
            if comp.level > max:
                max = comp.level

        return max

from baseintegration.exporter.processor import BaseProcessor
from jobscope.utils import ItemData, get_part_number_and_name
from baseintegration.datamigration import logger
from paperless.objects.orders import OrderComponent


class BOMProcessor(BaseProcessor):

    def _process(self, parts: list) -> None:
        self.parts = parts
        self.bom_sequence = 1
        for item in self.parts:
            item: ItemData = item
            if item.item_is_new and not item.component.is_hardware and len(item.component.child_ids) > 0:
                logger.info(f"Creating BOM for item {item.item_number}")
                self.get_child_bom(item.component)
            else:
                logger.info(f"Not creating BOM for item {item.item_number} as it is either old, hardware, or does not have any children")

    def get_child_bom(self, component: OrderComponent):
        if len(component.child_ids) == 0:
            return
        else:
            # reset bom sequence
            self.bom_sequence = 1
        for child in component.child_ids:
            item_data: ItemData = self.get_component_part_data(child)
            self.create_bom(component, item_data.component)
            self.bom_sequence = self.bom_sequence + 1
            if len(item_data.component.child_ids) > 0:
                self.get_child_bom(item_data.component)

    def get_component_part_data(self, component_id: int) -> ItemData:
        for p_data in self.parts:
            p_data: ItemData = p_data
            if p_data.component.id == component_id:
                return p_data
        else:
            raise ValueError("Could not find the necessary component in the list")

    def create_bom(self, parent_component: OrderComponent, child_component: OrderComponent):
        parent_item_number, _ = get_part_number_and_name(parent_component)
        child_item_number, _ = get_part_number_and_name(child_component)
        if child_component.is_hardware:
            psm = "P"
        else:
            psm = "M"
        self._exporter.client.create_bom_record(parent_item_number=parent_item_number,
                                                child_item_number=child_item_number,
                                                bom_sequence=self.bom_sequence,
                                                division_id="Jobscope",
                                                component_revision=child_component.revision,
                                                unit_of_issue="EA",
                                                quantity_per=child_component.make_quantity,
                                                psm=psm)

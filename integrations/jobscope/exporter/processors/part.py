from baseintegration.exporter import BaseProcessor
from paperless.objects.orders import Order, OrderItem, OrderComponent
from baseintegration.datamigration import logger
from jobscope.utils import ItemData, get_part_number_and_name


class PartProcessor(BaseProcessor):

    def _process(self, order: Order) -> list:
        logger.info("Processing parts")
        self.order = order
        self.parts = []
        logger.info("Iterating through each order item")
        # for each order item, iterate through all components and create a part if necessary
        for item in order.order_items:
            self.get_parts(item)
        return self.parts

    def get_parts(self, item: OrderItem):
        for component in item.components:
            logger.info(f"Checking component {component.part_name}")
            part: ItemData = self.get_or_create_part(component)
            self.parts.append(part)

    def get_or_create_part(self, component: OrderComponent) -> ItemData:
        part_number, part_name = get_part_number_and_name(component)
        logger.info(f"Checking for part with part number {str(part_number)}")
        part_number = str(part_number)[0:30]
        part = self._exporter.client.get_part(part_number)
        part_is_new = False
        # if part does not exist yet based on part number, create it in jobscope
        if not part:
            part_is_new = True
            logger.info(f"Part {part_number} not found, need to create a new part")
            if component.is_hardware:
                psm = "P"
            else:
                psm = "M"
            division_id = "Jobscope"
            unit_of_issue = "EA"
            logger.info(f"Part not found, creating part with part number {str(part_number)}")
            self._exporter.client.create_part(part_number,
                                              "MECHANICAL",
                                              psm,
                                              division_id,
                                              unit_of_issue,
                                              description=component.description,
                                              revision=component.revision)
        else:
            logger.info(f"Part {part_number} was found, not creating a new part")
        return ItemData(item_number=part_number, item_is_new=part_is_new, component=component)

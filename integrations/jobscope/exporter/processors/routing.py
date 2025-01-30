from baseintegration.exporter.processor import BaseProcessor
from jobscope.utils import ItemData
from baseintegration.datamigration import logger
from paperless.objects.orders import OrderOperation


class RoutingProcessor(BaseProcessor):

    def _process(self, parts: list) -> None:
        for item in parts:
            item: ItemData = item
            if item.item_is_new and not item.component.is_hardware:
                logger.info(f"Creating routing for item {item.item_number}")
                self.create_routing_header(item)
                self.create_operations(item)
                self.create_part_routing(item)
            else:
                logger.info(f"Not creating routing for item {item.item_number} as it is either old or hardware")

    def get_work_center_id(self, operation: OrderOperation):
        return operation.get_variable("WC ID")

    def get_work_center(self, operation: OrderOperation):
        return operation.get_variable("Work Center")

    def create_routing_header(self, item: ItemData):
        self._exporter.client.create_routing_header(item.item_number, item.component.revision,
                                                    item.component.description, "Jobscope")

    def create_part_routing(self, item: ItemData):
        self._exporter.client.create_part_routing(item.item_number, item.component.revision)

    def create_operations(self, item: ItemData) -> None:
        sequence_no = 10
        component = item.component
        operations = component.shop_operations
        logger.info(f"Processing operations for {str(component.part_number)}")
        for operation in operations:
            logger.info(f"Operations being processed for operation {operation.name}")
            work_center_id: str = self.get_work_center_id(operation)
            if not work_center_id:
                logger.info(
                    "Work center ID not found on operation. Must be an informational operation. Skipping and going to the next one")
                continue
            else:
                logger.info(f"Work center ID is {work_center_id}")
            work_center: str = self.get_work_center(operation)
            if not work_center:
                work_center = work_center_id
            setup_time = operation.setup_time if operation.setup_time else 0
            runtime = operation.runtime if operation.runtime else 0
            setup_hrs: float = round(setup_time, 2)
            run_hrs: float = round(runtime, 2)
            work_center_description = self.get_work_center_description(work_center)
            self._exporter.client.create_routing(item.item_number,
                                                 item.component.revision,
                                                 sequence_no,
                                                 work_center_id,
                                                 work_center_description,
                                                 setup_hrs,
                                                 run_hrs)
            sequence_no = sequence_no + 10

    def get_work_center_description(self, work_center: str):
        return None
